from django.db import models
from django.contrib.auth.models import User

from PIL import Image


GIOI_TINH = {
    "Nam": "Nam",
    "Nu": "Nữ",
    "Unisex": "Unisex",
}

class DanhMuc(models.Model):
    ten = models.CharField(max_length=50)
    kichhoat = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.id} - {self.ten}'

class SanPham(models.Model):
    ten = models.CharField(max_length=250)
    mota = models.TextField(null=True, blank=True)
    gia = models.FloatField(null=True, blank=True)
    gioitinh = models.CharField(max_length=10, choices=GIOI_TINH)
    ngaytao = models.DateTimeField(auto_now_add=True)
    kichhoat = models.BooleanField(default=True)
    hinhanh = models.ImageField(
        upload_to='uploads' # dir to store the image
    )
    danhmuc = models.ForeignKey(
        DanhMuc,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.id} - {self.ten}'
    
    

class LoaiSanPham(models.Model):
    mausac = models.CharField(max_length=55)
    hinhanh = models.ImageField(
        upload_to='uploads' # dir to store the image
    )
    sanpham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.id} - {self.mausac}'
    
   

class KichCoSanPham(models.Model):
    kichco = models.CharField(max_length=55)
    soluong = models.IntegerField(null=False, default=1)
    loaisanpham = models.ForeignKey(
        LoaiSanPham,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.id} - {self.kichco}'
    
class GioHang(models.Model):
    soluong = models.IntegerField(null=False, default=1)
    ngaythem = models.DateTimeField(auto_now_add=True)
    kichcosanpham = models.ForeignKey(
        KichCoSanPham,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.soluong}'

class DiaChi(models.Model):
    sdt = models.CharField(max_length=12)
    diachi = models.CharField(max_length=255)
    diachicuthe = models.TextField(null=True, blank=True)
    macdinh = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.sdt}'

class TrangThaiDonHang(models.Model):
    trangthai = models.CharField(max_length=55)
    def __str__(self):
        return f'{self.id} - {self.trangthai}'

class PhuongThucThanhToan(models.Model):
    ten = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.id} - {self.ten}'
   

class DonHang(models.Model):
    tongtien = models.FloatField(null=True, blank=True)
    ngaytao = models.DateTimeField(auto_now_add=True)
    ngaysua = models.DateTimeField(null=True)

    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    trangthaidonhang = models.ForeignKey(
        TrangThaiDonHang,
        on_delete=models.CASCADE
    )
    phuongthucthanhtoan = models.ForeignKey(
        PhuongThucThanhToan,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return f'{self.id} - {self.tongtien}'


class ThongTinDonHang(models.Model):
    hoten = models.CharField(max_length=100)
    sdt = models.CharField(max_length=12)
    diachinhanhang = models.TextField(blank=True)
    donhang = models.OneToOneField(DonHang, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.donhang} - {self.sdt}'

class ChiTietDonHang(models.Model):
    gia = models.FloatField(blank=True)
    soluong = models.IntegerField(blank=True)

    donhang = models.ForeignKey(
        DonHang,
        on_delete=models.CASCADE
    )
    kichcosanpham = models.ForeignKey(
        KichCoSanPham,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.id}'
    
class DanhGiaSanPham(models.Model):
    sosao = models.IntegerField()
    binhluan = models.TextField(blank=True)

    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    chitietdonhang = models.ForeignKey(
        ChiTietDonHang,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.id}'
        


        


