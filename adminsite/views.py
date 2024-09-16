from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, F, Sum, Count
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.core import serializers
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User 
from .forms import (
   LoginForm,
   KhachHangForm,
   SanPhamForm,
   DanhMucForm,
)
from app.models import (
   SanPham, 
   DanhMuc, 
   LoaiSanPham,
   KichCoSanPham,
   GioHang,
   DiaChi,
   DonHang,
   ChiTietDonHang,
   ThongTinDonHang,
)


from django.contrib.auth.decorators import login_required

from django.utils import timezone

from django.db.models.functions import ExtractMonth, ExtractYear

@login_required
def dashboard(request):
    slkhachhang = User.objects.filter(is_superuser=False).count()
    slsanpham = SanPham.objects.count()
    sldonhang = DonHang.objects.count()
    tongtienhang = DonHang.objects.aggregate(total_tienhang=Sum('tongtien'))['total_tienhang']

    tongtienUser = DonHang.objects.select_related("user").values('user__username').annotate(total_tongtien=Sum('tongtien'))

    current_date = timezone.now()

    results = DonHang.objects.filter(ngaysua__year=current_date.year, trangthaidonhang_id=3).\
                annotate(thang=ExtractMonth('ngaysua')).\
                values('thang').\
                annotate(tongtien=Sum('tongtien')).\
                order_by('thang')
    return render(request, 'pages/dashboard.html',
                  {
                     "slkhachhang": slkhachhang,
                     "slsanpham": slsanpham,
                     "sldonhang": sldonhang,
                     "tongtienhang": tongtienhang,
                     "tongtienUser": tongtienUser,
                     "thongkedtJson": results
                  })

def admin_dangnhap(request):
    if request.method == 'GET':
        form = LoginForm()
        if request.user.is_authenticated:
           if request.user.is_superuser:
            return redirect("/admin/dashboard/")
        return render(request,'pages/dangnhap.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user and user.is_superuser:
                login(request, user)    
                return redirect('/admin/dashboard/')
        # form is not valid or user is not authenticated
        messages.error(request,f'Tên người dùng và mật khẩu không chính xác!')
        return render(request,'pages/dangnhap.html',{'form': form})

@login_required
def admin_dangxuat(request):
    logout(request)
    return redirect("/admin/")
    # Redirect to a success page.

@login_required
def danhmuc(request):
  dsdanhmuc=DanhMuc.objects.all()
  return render(request, 'pages/danhmuc.html',{'dsdanhmuc': dsdanhmuc})

@login_required
def suadanhmuc(request, id):
    danhmuc = get_object_or_404(DanhMuc, id=id)
    if request.method == 'POST':
        form = DanhMucForm(request.POST, instance=danhmuc)
        if form.is_valid():
            form.save(danhmuc)
            return redirect('danhmuc')  # Điều hướng tới trang danh mục
    else:
        form = DanhMucForm(instance=danhmuc)
    return render(request, 'pages/suadanhmuc.html', {'form': form})




@login_required
def xoadanhmuc(request, id):
    danhmuc = get_object_or_404(DanhMuc, id=id)
    
    if request.method == 'POST':
        danhmuc.delete()
        return redirect('danhmuc')  # Điều hướng tới trang danh mục sau khi xóa thành công
    
    return render(request, 'pages/xoadanhmuc.html', {'danhmuc': danhmuc})


@login_required
def themdanhmuc(request):
  if request.method == 'POST':
    form = DanhMucForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('danhmuc')
  else:
    form = DanhMucForm()
  return render(request, 'pages/themdanhmuc.html',{'form': form})


@login_required
def qlsanpham(request):
    san_phams = SanPham.objects.all()
    return render(request, 'pages/sanpham.html', {'san_phams': san_phams})

@login_required
def themsanpham(request):
    if request.method == "POST":
        form = SanPhamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('qlsanpham')
    else:
        form = SanPhamForm()
    return render(request, 'pages/themsanpham.html', {'form': form})


@login_required
def suasanpham(request, sanpham_id):
    san_pham = get_object_or_404(SanPham, id=sanpham_id)
    if request.method == 'POST':
        form = SanPhamForm(request.POST, request.FILES, instance=san_pham)
        if form.is_valid():
            form.save()
            return redirect('qlsanpham')
    else:
        form = SanPhamForm(instance=san_pham)
    return render(request, 'pages/suasanpham.html', {'form': form})

@login_required
def xoasanpham(request, sanpham_id):
    san_pham = get_object_or_404(SanPham, id=sanpham_id)
    if request.method == 'POST':
        san_pham.delete()
        return redirect('qlsanpham')
    return render(request, 'pages/confirm_xoa.html', {'san_pham': san_pham})
#đưa dòng này lên đầu file 

@login_required
def khachhang(request):
  khach_hangs = User.objects.filter(is_superuser=False)
  return render(request, 'pages/khachhang.html',{'khach_hangs': khach_hangs})

@login_required
def themkhachhang(request):
  if request.method == 'POST':
    form = KhachHangForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('khachhang')
  else:
    form = KhachHangForm()
  return render(request, 'pages/themkhachhang.html',{'form': form})


@login_required
def suakhachhang(request, khachhang_id):
    khach_hang = get_object_or_404(User, id=khachhang_id)
    passs = khach_hang.password;
    if request.method == 'POST':
        form = KhachHangForm(request.POST, instance=khach_hang)
        if form.is_valid():
            form.save()
            return redirect('khachhang')
    else:
        form = KhachHangForm(instance=khach_hang)
    return render(request, 'pages/suakhachhang.html', {'form': form})

@login_required
def xoa_khachhang(request, khachhang_id):
    khach_hang = get_object_or_404(User, id=khachhang_id)
    if request.method == 'POST':
        khach_hang.delete()
        return redirect('khachhang')
    return render(request, 'pages/xoakhachhang.html', {'khach_hang': khach_hang})



@login_required
def XacNhanDonHang(request):
    if request.method == 'GET':
        # paginate_by=8
        dsdonhang = DonHang.objects.select_related('thongtindonhang', 'user').filter(trangthaidonhang_id=1).all().order_by("-ngaytao");
        return render(request, 'pages/xacnhandonhang.html', {'dsdonhang': dsdonhang})
    elif request.method == 'POST':
       dhid = request.POST.get("orderId", "");
       trangthaiId = -1;
       if request.POST.get("order-confirm", "") == "Từ chối":
          trangthaiId = 4
       else:
          trangthaiId = 2
       dc = DonHang.objects.filter(Q(id=dhid)).first();
       dc.trangthaidonhang_id = trangthaiId
       dc.ngaysua = timezone.now()
       dc.save()   
       return HttpResponseRedirect(request.path_info)
    
@login_required
def DonHangVanChuyen(request):
    if request.method == 'GET':
        # paginate_by=8
        dsdonhang = DonHang.objects.select_related('thongtindonhang', 'user').filter(trangthaidonhang_id=2).all().order_by("-ngaysua");
        return render(request, 'pages/donhangdangvanchuyen.html', {'dsdonhang': dsdonhang})
    elif request.method == 'POST':
       dhid = request.POST.get("orderId", "");
       trangthaiId = -1;
       if request.POST.get("order-confirm", "") == "Hủy đơn":
          trangthaiId = 4
       else:
          trangthaiId = 3
       dc = DonHang.objects.filter(Q(id=dhid)).first();
       dc.trangthaidonhang_id = trangthaiId
       dc.ngaysua = timezone.now()
       dc.save()   
       return HttpResponseRedirect(request.path_info)
       
@login_required
def DonHangHoanThanh(request):
    if request.method == 'GET':
        # paginate_by=8
        dsdonhang = DonHang.objects.select_related('thongtindonhang', 'user').filter(trangthaidonhang_id=3).all().order_by("-ngaysua");
        return render(request, 'pages/donhanghoanthanh.html', {'dsdonhang': dsdonhang})
    

@login_required
def DonHangDaHuy(request):
    if request.method == 'GET':
        # paginate_by=8
        dsdonhang = DonHang.objects.select_related('thongtindonhang', 'user').filter(trangthaidonhang_id=4).all().order_by("-ngaysua");
        return render(request, 'pages/donhangdahuy.html', {'dsdonhang': dsdonhang})
    


