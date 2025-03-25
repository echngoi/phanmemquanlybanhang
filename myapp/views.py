
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


# hàm xử lý edit sản phẩm

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
    products = Product.objects.all()
    return render(request, 'tao_don_hang.html', {'products': products})