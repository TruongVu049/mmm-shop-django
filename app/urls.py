from django.urls import path
from .views import (
    index, 
    DSSanPham, 
    lienhe, 
    DangKy, 
    DangNhap,
    ChiTietSanPham,
    LayDsKichCoSanPham,
    DangXuat,
    LaySpGioHang,
    LaySlSpGioHang,
    ThemSpGiohang,
    ThongTinNguoiDung,
    DiaChiNguoiDung,
    giohang,
    GioHangNguoiDung,
    thanhtoan,
    thanhtoan_,
    donhang,
    LayDsDonHang,
    HuyDonHang,
    LayDonHangId,
    
)

urlpatterns = [
    path('', index, name="index"),
    path('sanpham/', DSSanPham.as_view(),name='sanpham'),
    path('chitietsanpham/<slug:pk>/',ChiTietSanPham.as_view(),name="chitietsanpham"),
    path('lienhe/', lienhe, name="lienhe"),
    path('dangky/', DangKy.as_view(),name='dangky'),
    path('dangnhap/', DangNhap,name='dangnhap'),
    path('dangxuat/', DangXuat,name='dangxuat'),
    path('thongtin/', ThongTinNguoiDung,name='thongtin'),
    path('giohang/', giohang,name='giohang'),
    path('thanhtoan/', thanhtoan,name='thanhtoan'),
    path('thanhtoan_/', thanhtoan_,name='thanhtoan_'),
    path('donhang/', donhang,name='donhang'),

    # ==================== API ======================
    
    
    
    path('kichcosanpham/<int:pk>/', LayDsKichCoSanPham, name='kichcosanpham'),
    path('layspgiohang/<int:pk>/<int:page>/<int:limit>', LaySpGioHang, name='layspgiohang'),
    path('layslspgiohang/', LaySlSpGioHang, name='layslspgiohang'),
    path('themspgiohang/', ThemSpGiohang, name='themspgiohang'),
    path('themspgiohang/', ThemSpGiohang, name='themspgiohang'),
    path('diachinguoidung/<int:pk>/', DiaChiNguoiDung, name='diachinguoidung'),
    path('giohangnguoidung/', GioHangNguoiDung, name='giohangnguoidung'),
    path('donhang/<int:trangthaiId>/', LayDsDonHang, name='donhang'),
    path('huydonhang/', HuyDonHang, name='huydonhang'),
    path('laydonhangid/<int:iddh>/', LayDonHangId, name='laydonhangid'),



]