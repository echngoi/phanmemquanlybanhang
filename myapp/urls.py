from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('addpro', views.add_product, name='add_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product/add/', views.them_sanpham, name='them_sanpham'),

    path('don-hang/tao/', views.tao_don_hang, name='tao_don_hang'),
    path('don-hang/xem/', views.xem_don_hang, name='xem_don_hang'),
    path('don-hang/chinh-sua/<int:don_hang_id>/', views.chinh_sua_don_hang, name='chinh_sua_don_hang'),
    path('don-hang/xoa/<int:don_hang_id>/', views.xoa_don_hang, name='xoa_don_hang'),
    path('tim-kiem-san-pham/', views.tim_kiem_san_pham, name='tim_kiem_san_pham'),

    path('don-hang/<int:don_hang_id>/in-hoa-don/', views.in_hoa_don, name='in_hoa_don'),
    path('don-hang/<int:don_hang_id>/xem-truoc-hoa-don/', views.xem_truoc_hoa_don, name='xem_truoc_hoa_don'),
]
