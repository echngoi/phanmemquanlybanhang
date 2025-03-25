from django.urls import path
from . import views

urlpatterns = [

    # xử lý các url thêm sản phẩm vào database
    path('', views.product_list, name='product_list'),
    path('addpro', views.add_product, name='add_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product/add/', views.them_sanpham, name='them_sanpham'),


    #xử lý các url tạo đơn hàng mới
    path('don-hang/tao/', views.tao_don_hang, name='tao_don_hang'),
   
   
    
]
