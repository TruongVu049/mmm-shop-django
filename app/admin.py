from django.contrib import admin

# Register your models here.
from .models import (
    DanhMuc,
    SanPham,
    LoaiSanPham,
    KichCoSanPham,
    GioHang,
    DiaChi,
    TrangThaiDonHang,
    PhuongThucThanhToan,
    DonHang,
    ThongTinDonHang,
    ChiTietDonHang,
    DanhGiaSanPham,
)

admin.site.register(DanhMuc)
admin.site.register(SanPham)
# admin.site.register(LoaiSanPham)
# admin.site.register(KichCoSanPham)
admin.site.register(GioHang)
admin.site.register(DiaChi)
admin.site.register(TrangThaiDonHang)
admin.site.register(PhuongThucThanhToan)
admin.site.register(DonHang)
admin.site.register(ThongTinDonHang)
admin.site.register(ChiTietDonHang)
admin.site.register(DanhGiaSanPham)


class KichCoSanPhamInline(admin.TabularInline):
    model = KichCoSanPham
    extra = 1

class LoaiSanPhamAdmin(admin.ModelAdmin):
    inlines = [KichCoSanPhamInline]

admin.site.register(LoaiSanPham, LoaiSanPhamAdmin)