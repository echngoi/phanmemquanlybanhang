
from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Category
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from .models import DonHang, ChiTietDonHang, KhachHang
from .forms import DonHangForm, ChiTietDonHangForm, KhachHangForm
from django.db import transaction

from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit



    
# thêm hàng hóa code trang riêng demo
def add_product(request):
    if request.method == 'POST':
            name = request.POST['name']
            code = request.POST['code']
            price = request.POST['price']
            stock = request.POST['stock']
            image = request.POST['image']
            category = request.POST['category']
            brand = request.POST['brand']
            import_date = request.POST['import_date']
            # Tạo sản phẩm mới
            Product.objects.create(name=name, code=code, price=price, stock=stock, image=image, category=category, brand=brand, import_date=import_date)
            return redirect('product_list')
    return render(request, 'add_product.html')

# them hang hóa cho modal
@csrf_exempt
def them_sanpham(request):
    categories = Category.objects.all()  # Lấy tất cả các phân loại
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            code = request.POST.get('code')
            price = request.POST.get('price')
            stock = int( request.POST.get('stock',0))
            category_id = request.POST.get('category')
            brand = request.POST.get('brand')
            import_date = request.POST.get('import_date')
            category = Category.objects.get(id=category_id)

            # Tìm kiếm sản phẩm hiện có
            sanpham = Product.objects.filter(code=code, name=name).first()

            if sanpham:
                # Sản phẩm tồn tại, cập nhật số lượng
                sanpham.stock += stock
                sanpham.save()

            else:   # Tạo sản phẩm mới
                sanpham = Product(name=name, code=code, price=price,stock = stock, category=category, brand=brand, import_date=import_date)
                sanpham.save()

            return JsonResponse({'status': 'success', 'message': 'Thêm sản phẩm thành công!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return render(request, 'product_list.html', {'categories': categories})

# hiển thị danh sách hàng hóa
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

   
    name = request.GET.get('name')
    code = request.GET.get('code')
    search = request.GET.get('search')
    
    if code:
        products = products.filter(code=code)
    if name:
        products = products.filter(name__icontains=name)
    if search:
        products = products.filter(
            Q(code__icontains=search) |
            Q(name__icontains=search) |
            Q(price__icontains=search) |
            Q(category__icontains=search) |
            Q(brand__icontains=search) |
            Q(import_date__icontains=search)
        )
    paginator = Paginator(products,12)  # Hiển thị 10 bệnh nhân trên mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'code': code,
        'name': name,
        'search': search,
        'categories': categories,
    }


    return render(request, 'product_list.html', context)


# hàm xử lý edit bệnh nhân

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        print(request.POST) # In dữ liệu nhận được
        try:
            product.name = request.POST.get('name')
            product.code = request.POST.get('code')
            product.price = float(request.POST.get('price')) # Chuyển đổi sang float
            product.category = request.POST.get('category')
            product.brand = request.POST.get('brand')
            product.import_date = datetime.strptime(request.POST.get('import_date'), '%d/%m/%Y').date() # Chuyển đổi sang date
            product.save()
            return JsonResponse({'status': 'success', 'product': {
                'id': product.id,
                'name': product.name,
                'code': product.code,
                'price': product.price,
                'category': product.category,
                'brand': product.brand,
                'import_date': product.import_date.strftime('%Y-%m-%d'),
            }})
        except ValueError as ve:
            return JsonResponse({'status': 'error', 'message': f'Lỗi kiểu dữ liệu: {str(ve)}'})
        except Exception as e:
            print(e) # In lỗi chi tiết ra console
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
    # xử lý nút chức năng nút xóa sản phẩm
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'DELETE':
        try:
            product.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# xử lý chức năng tạo đơn hàng

def tao_don_hang(request):
    products = Product.objects.all() # Lấy danh sách sản phẩm

    if request.method == 'POST':
        ten_khach_hang = request.POST.get('ten_khach_hang')
        so_dien_thoai = request.POST.get('so_dien_thoai')
        san_phams = request.POST.getlist('san_pham[]')
        so_luongs = request.POST.getlist('so_luong[]')

        with transaction.atomic():
            khach_hang = KhachHang.objects.create(ten=ten_khach_hang, so_dien_thoai=so_dien_thoai)
            don_hang = DonHang.objects.create(khach_hang=khach_hang, tong_tien=0)

            tong_tien = 0
            for i in range(len(san_phams)):
                san_pham = Product.objects.get(id=san_phams[i])
                so_luong = int(so_luongs[i])
                gia = san_pham.price
                ChiTietDonHang.objects.create(don_hang=don_hang, san_pham=san_pham, so_luong=so_luong, gia=gia)
                tong_tien += so_luong * gia

            don_hang.tong_tien = tong_tien
            don_hang.save()

        return redirect('xem_don_hang')

    return render(request, 'tao_don_hang.html', {'products': products})

# xem đơn hàng
def xem_don_hang(request):
    don_hangs = DonHang.objects.all()
    return render(request, 'xem_don_hang.html', {'don_hangs': don_hangs})

# chỉnh sửa đơn hàng
def chinh_sua_don_hang(request, don_hang_id):
    don_hang = DonHang.objects.get(pk=don_hang_id)
    if request.method == 'POST':
        form = DonHangForm(request.POST, instance=don_hang)
        if form.is_valid():
            form.save()
            return redirect('xem_don_hang')
    else:
        form = DonHangForm(instance=don_hang)
    return render(request, 'chinh_sua_don_hang.html', {'form': form})

# Xóa đơn hàng
def xoa_don_hang(request, don_hang_id):
    don_hang = DonHang.objects.get(pk=don_hang_id)
    don_hang.delete()
    return redirect('xem_don_hang')

# Tìm kiếm sản phẩm
def tim_kiem_san_pham(request):
    ma_san_pham = request.GET.get('ma')
    ten_san_pham = request.GET.get('ten')

    if ma_san_pham:
        san_phams = Product.objects.filter(code__icontains=ma_san_pham)
    elif ten_san_pham:
        san_phams = Product.objects.filter(name__icontains=ten_san_pham)
    else:
        return JsonResponse({'san_phams': []})

    data = {
        'san_phams': [{
            'id': san_pham.id,
            'ten': san_pham.name,
            'ma': san_pham.code,
        } for san_pham in san_phams]
    }
    return JsonResponse(data)

# in hóa đơn

def in_hoa_don(request, don_hang_id):
    don_hang = get_object_or_404(DonHang, pk=don_hang_id)
    chi_tiet_don_hang = don_hang.chitietdonhang_set.all()
    
    # Tính toán tổng tiền cho từng chi tiết
    tong_tien_chi_tiet = [chi_tiet.so_luong * chi_tiet.gia for chi_tiet in chi_tiet_don_hang]

    context = {
        'don_hang': don_hang,
        'tong_tien_chi_tiet': tong_tien_chi_tiet,
    }
    return HttpResponse(render_to_string('hoa_don.html', context)) #Sử dụng render_to_string để tạo html_string và trả về HttpResponse
# xem trước hóa đơn

def xem_truoc_hoa_don(request, don_hang_id):
    don_hang = get_object_or_404(DonHang, pk=don_hang_id)
    chi_tiet_don_hang = don_hang.chitietdonhang_set.all()
    
    # Tính toán tổng tiền cho từng chi tiết
    tong_tien_chi_tiet = [chi_tiet.so_luong * chi_tiet.gia for chi_tiet in chi_tiet_don_hang]

    context = {
        'don_hang': don_hang,
        'tong_tien_chi_tiet': tong_tien_chi_tiet,
    }
    return render(request, 'hoa_don.html', context)