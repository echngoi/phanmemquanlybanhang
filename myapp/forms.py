from django import forms
from .models import DonHang, ChiTietDonHang, KhachHang

class KhachHangForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = '__all__'

class DonHangForm(forms.ModelForm):
    class Meta:
        model = DonHang
        fields = ['khach_hang', 'trang_thai']

class ChiTietDonHangForm(forms.ModelForm):
    class Meta:
        model = ChiTietDonHang
        fields = ['san_pham', 'so_luong', 'gia']