from django.urls import path
from .views import (
    admin_dangnhap, 
    dashboard,
    admin_dangxuat,
    
    danhmuc,
    suadanhmuc,
    themdanhmuc,
    xoadanhmuc,

    qlsanpham,
    themsanpham,
    suasanpham,
    xoasanpham,

    khachhang,
    themkhachhang,
    suakhachhang,
    xoa_khachhang,
    

    XacNhanDonHang,
    DonHangVanChuyen,
    DonHangHoanThanh,
    DonHangDaHuy
)

urlpatterns = [
    path('', admin_dangnhap, name="admin_dangnhap"),
    path('dashboard/', dashboard, name="dashboard"),
    path('admin_dangxuat/', admin_dangxuat, name="admin_dangxuat"),

    path('danhmuc/', danhmuc, name="danhmuc"),
    path('themdanhmuc/', themdanhmuc, name="themdanhmuc"),
    path('suadanhmuc/<int:id>/', suadanhmuc, name="suadanhmuc"),
    path('xoadanhmuc/<int:id>/', xoadanhmuc, name="xoadanhmuc"),

    path('qlsanpham/', qlsanpham, name="qlsanpham"),
    path('themsanpham/', themsanpham, name="themsanpham"),
    path('suasanpham/<int:sanpham_id>/', suasanpham, name="suasanpham"),
    path('xoasanpham/<int:sanpham_id>/', xoasanpham, name="xoasanpham"),  # Thêm đường dẫn cho chức năng xóa sản phẩm

    #ngoc
    path('khachhang/', khachhang, name="khachhang"),
    path('themkhachhang/', themkhachhang, name="themkhachhang"),
    path('suakhachhang/<int:khachhang_id>/', suakhachhang, name="suakhachhang"),
    path('xoakhachhang/<int:khachhang_id>/', xoa_khachhang, name="xoakhachhang"),

    path('donhangchoxacnhan/', XacNhanDonHang, name="donhangchoxacnhan"),
    path('donhangdangvanchuyen/', DonHangVanChuyen, name="donhangdangvanchuyen"),
    path('donhanghoanthanh/', DonHangHoanThanh, name="donhanghoanthanh"),
    path('donhangdahuy/', DonHangDaHuy, name="donhangdahuy"),


]