from django.db import models



class KhachHang(models.Model):
    ten = models.CharField(max_length=255)
    dia_chi = models.TextField()
    so_dien_thoai = models.CharField(max_length=20)

    def __str__(self):
        return self.ten
    
class DonHang(models.Model):
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    tong_tien = models.DecimalField(max_digits=10, decimal_places=2)
    trang_thai = models.CharField(max_length=50, default='Đang chờ xử lý')

    def __str__(self):
        return f"Đơn hàng {self.id} - {self.khach_hang.ten}"

    
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    import_date = models.DateField()

    def __str__(self):
        return self.name

class ChiTietDonHang(models.Model):
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE)
    san_pham = models.ForeignKey(Product, on_delete=models.CASCADE)
    so_luong = models.PositiveIntegerField()
    gia = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.san_pham.name} - {self.so_luong}"