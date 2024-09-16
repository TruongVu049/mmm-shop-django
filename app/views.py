from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.db.models import Q, F, Avg, Count, Sum, Subquery, OuterRef
from django.urls import reverse_lazy
from django.contrib import messages

from django.http import JsonResponse
import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import login, authenticate, logout

from .forms import (
   RegisterForm,
   LoginForm
)

from .models import (
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
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone


def index(request):
    order_details_subquery = ChiTietDonHang.objects.filter(donhang__trangthaidonhang_id=3).values('kichcosanpham__loaisanpham__sanpham_id').annotate(
        sales_count=Count('kichcosanpham__loaisanpham__sanpham_id')
    ).values('kichcosanpham__loaisanpham__sanpham_id', 'sales_count')
    # Step 2: Aggregate the results at the product size level
    product_size_aggregation = (
        KichCoSanPham.objects
        .values('loaisanpham__sanpham_id')
        .annotate(
            total_sales=Sum(Subquery(order_details_subquery.values('sales_count')))
        )
    )
    top_products_query = (
        SanPham.objects
        .annotate(
            total_sales=Subquery(
                product_size_aggregation.filter(
                    loaisanpham__sanpham_id=OuterRef('pk')
                ).values('total_sales')
            )
        )
        .order_by('-total_sales')[:5]
        .values('id', 'ten', 'gia', 'gioitinh', 'ngaytao', 'danhmuc_id', 'hinhanh', 'total_sales')
    )
    re_products=SanPham.objects.all().order_by('-ngaytao')[:5]

    return render(request, 'page/index.html', {'top_products': top_products_query, 're_products': re_products })



class DSSanPham(ListView):
  model = SanPham
  context_object_name = 'dssanpham'
  template_name = "page/sanpham.html"
  paginate_by=8
  def get_queryset(self):
      danhmucs = DanhMuc.objects.all().values_list("id");
      tk = self.request.GET.get("s","")
      sx=self.request.GET.get("sx","")
      ft_danhmuc = self.request.GET.getlist("ft_danhmuc", danhmucs);
      ft_gioitinh = self.request.GET.getlist("ft_gioitinh", ["Nam", "Nu", "Unisex"]);
      giaNN = self.request.GET.get("gia_nn", 0);
      giaLN = self.request.GET.get("gia_ln", 3000000);
      
      dssanpham = []
      if tk != "":
        dssanpham=SanPham.objects.all().filter(Q(ten__icontains=tk), Q(danhmuc__in=ft_danhmuc), Q(gioitinh__in=ft_gioitinh), Q(gia__range=(float(giaNN),float(giaLN))), Q(kichhoat=True))
      else:
        dssanpham=SanPham.objects.all().filter(Q(danhmuc__in=ft_danhmuc), Q(gioitinh__in=ft_gioitinh), Q(gia__range=(float(giaNN),float(giaLN))), Q(kichhoat=True))
      if(sx != ""):
          sx = sx.split("_")
          if(sx[1] == "desc"):
            dssanpham = dssanpham.order_by(f'-{sx[0]}')
          else:
            dssanpham = dssanpham.order_by(f'{sx[0]}')
        
      return dssanpham
      
  def get_context_data(self,**kwargs):
      context=super(DSSanPham,self).get_context_data(**kwargs)
      context["danhmucs"]= DanhMuc.objects.all();
      context["tk"]=self.request.GET.get("s","")
      context["sx"]=self.request.GET.get("sx","")
      context["ft_danhmuc"] = self.request.GET.getlist("ft_danhmuc", []);
      context["ft_danhmuc"] = list(map(int, context["ft_danhmuc"]))
      context["ft_gioitinh"] = self.request.GET.getlist("ft_gioitinh", []);
      context["gia_nn"] = self.request.GET.get("gia_nn", 0);
      context["gia_ln"] = self.request.GET.get("gia_ln", 3000000);
      return context


class ChiTietSanPham(DetailView):
    model = SanPham
    context_object_name = 'sanpham'
    template_name = "page/chitietsanpham.html"

    def get_context_data(self,**kwargs):
      context=super(ChiTietSanPham,self).get_context_data(**kwargs)
      sanpham_id=self.kwargs['pk']
      loaisanpham = LoaiSanPham.objects.all().filter(sanpham__id=sanpham_id).values();
      context['loaisanpham'] = loaisanpham
      context['sanphamlienquan'] = SanPham.objects.all().filter(Q(danhmuc__id=context['sanpham'].danhmuc_id), ~Q(id__icontains=context['sanpham'].id))[:5]
      return context

def lienhe(request):
  return render(request, 'page/lienhe.html')


class DangKy(FormView):
    template_name = 'page/dangky.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')
    redirect_authenticated_user=True
    def form_valid(self, form):
        user = form.save()
        if user:
            return redirect("/dangnhap")
            
        return super(DangKy, self).form_valid(form)
    

def DangNhap(request):
    if request.method == 'GET':
        form = LoginForm()
        if request.user.is_authenticated:
           return redirect("/")
        return render(request,'page/dangnhap.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user and not user.is_superuser:
                login(request, user)    
                return redirect('index')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Tên người dùng và mật khẩu không chính xác!')
        return render(request,'page/dangnhap.html',{'form': form})

@login_required
def DangXuat(request):
    logout(request)
    return redirect("/")
    # Redirect to a success page.

@login_required
def ThongTinNguoiDung(request):
    if request.method == "GET":
        return render(request, 'page/thongtin.html')
    elif request.method == "POST":
        typeCheckout = request.POST.get("typeCheckout")
        if typeCheckout == "1":
            context={
                "typeCheckout": typeCheckout,
                "size": request.POST.get("size"),
                "quantity": request.POST.get("quantity"),
            }
            return render(request, 'page/thongtin.html', context)
        else:
            context={
                "typeCheckout": typeCheckout,
                "dsspId": request.POST.get("dsspId"),
            }
            return render(request, 'page/thongtin.html', context)

@login_required
def giohang(request):
  return render(request, 'page/giohang.html')

@login_required
def thanhtoan(request):
  if request.method == 'POST':
    typeCheckOut = request.POST.get('typeCheckout')
    if typeCheckOut == '1':
        quantity = int(request.POST.get("quantity"))
        kichcosanphamId = request.POST.get("size", "-1")
        dssanpham = KichCoSanPham.objects.select_related('loaisanpham__sanpham').filter(id=kichcosanphamId).values(
        spid=F('loaisanpham__sanpham__id'),
        ten=F('loaisanpham__sanpham__ten'),
        gia=F('loaisanpham__sanpham__gia'),
        hinhanh=F('loaisanpham__hinhanh'),
        mausac=F('loaisanpham__mausac'),
        kichcosp=F('kichco'),
        kcspid=F('id'),
        tong=F("loaisanpham__sanpham__gia") * quantity,
        )
        tongtien = sum(item['tong'] for item in dssanpham)
        dsDiaChi = DiaChi.objects.filter(user_id=request.user.id).all().order_by("-id")
        data= {
            'size': kichcosanphamId,
            'quantity': quantity,
            'typeCheckout': typeCheckOut
        }
        dsdiachiJson = serializers.serialize("json", dsDiaChi)
        return render(request, 'page/thanhtoan.html', context={"dssp": dssanpham, 'quantity': quantity, 'tongtien': tongtien, "dsDiaChi": dsDiaChi, "data": data, "dsdiachiJson": dsdiachiJson})
    elif typeCheckOut == '0':
        dsspId = request.POST.get("dsspck")
        dsspId = json.loads(dsspId)
        dssanpham = GioHang.objects.select_related('kichcosanpham__loaisanpham__sanpham').filter(Q(kichcosanpham_id__in=dsspId)).values(
        spid=F('kichcosanpham__loaisanpham__sanpham__id'),
        ten=F('kichcosanpham__loaisanpham__sanpham__ten'),
        gia=F('kichcosanpham__loaisanpham__sanpham__gia'),
        hinhanh=F('kichcosanpham__loaisanpham__hinhanh'),
        mausac=F('kichcosanpham__loaisanpham__mausac'),
        kichcosp=F('kichcosanpham__kichco'),
        kcspid=F('kichcosanpham__id'),
        soluongg=F('soluong'),
        tong=F("kichcosanpham__loaisanpham__sanpham__gia") * F('soluong'),
        )
        tongtien = sum(item['tong'] for item in dssanpham)
        dsDiaChi = DiaChi.objects.filter(user_id=request.user.id).all().order_by("-id")
        data= {
            'typeCheckout': typeCheckOut
        }
        dsspId = request.POST.get("dsspck")
        dsdiachiJson = serializers.serialize("json", dsDiaChi)
        return render(request, 'page/thanhtoan.html', context={"dssp": dssanpham, 'tongtien': tongtien, "dsDiaChi": dsDiaChi, "data": data, "dsdiachiJson": dsdiachiJson, "dsspId": dsspId})



@login_required
def thanhtoan_(request):
    try:
        if request.method == "POST":
            diachiId = request.POST.get("addressId")
            diachi = DiaChi.objects.get(id=diachiId)
            dsspsl = request.POST.getlist("sp[]")
            dsspsl = [[int(item.split('_')[0]), int(item.split('_')[1])] for item in dsspsl]
            dsspId = [item[0] for item in dsspsl]
            dssp = KichCoSanPham.objects.select_related('loaisanpham__sanpham').filter(id__in=dsspId).values(
            spid=F('loaisanpham__sanpham__id'),
            kcspid=F('id'),
            gia=F("loaisanpham__sanpham__gia"),
            )
            counter = 0
            tongtien = 0
            for item in dssp:
                tongtien += item['gia'] * dsspsl[counter][1]
                counter+=1
            themHoaDon = DonHang.objects.create(
                        tongtien=tongtien,
                        user_id=request.user.id,
                        trangthaidonhang_id=1,
                        phuongthucthanhtoan_id=1,
                    )
            themHoaDon.save()
            themThongTinDonHang = ThongTinDonHang.objects.create(
                        hoten=request.user.username,
                        sdt=diachi.sdt,
                        diachinhanhang=(diachi.diachicuthe + ", " + diachi.diachi),
                        donhang_id=themHoaDon.id,
                    )
            themThongTinDonHang.save()

            counter = 0
            for item in dssp:
                themChiTietDonHang = ChiTietDonHang.objects.create(
                            gia=item['gia'],
                            soluong=dsspsl[counter][1],
                            donhang_id=themHoaDon.id,
                            kichcosanpham_id=item['kcspid'],
                        )
                themChiTietDonHang.save()
                counter+=1  
    except ObjectDoesNotExist:
        return render(request, 'page/thanhtoan_.html', {"trangthai": False})
    else:
        return render(request, 'page/thanhtoan_.html', {"trangthai": True})


@login_required
def donhang(request):
  return render(request, 'page/donhang.html')


# =========================== API =====================================
def LayDsKichCoSanPham(request, pk):
    try:
        # find todo by id
        kichcosanpham = KichCoSanPham.objects.all().filter(loaisanpham__id = pk)
    except ObjectDoesNotExist:
        # return 404 if the todo does not exists
        return JsonResponse({
            'status_code': 404,
            'error': f'Todo with id {pk} not found.'
        })
    else:
        # prepare data to return
        data = {'kichcosanpham': list(kichcosanpham.values())}
        # return JSON
        return JsonResponse(data)
    
@login_required
def LaySpGioHang(request, pk, page, limit):
    try:
        spgiohang = GioHang.objects.select_related('kichcosanpham__loaisanpham__sanpham').filter(user_id=request.user.id).values(
        spid=F('kichcosanpham__loaisanpham__sanpham__id'),
        ten=F('kichcosanpham__loaisanpham__sanpham__ten'),
        gia=F('kichcosanpham__loaisanpham__sanpham__gia'),
        hinhanh=F('kichcosanpham__loaisanpham__hinhanh'),
        mausac=F('kichcosanpham__loaisanpham__mausac'),
        kichco=F('kichcosanpham__kichco'),
        kcspid=F('kichcosanpham__id'),
        soluongg=F('soluong'),
        ).order_by("-ngaythem")[page:limit]
        
    except ObjectDoesNotExist:
        return JsonResponse({
            'status_code': 404,
            'error': f'Todo with id {pk} not found.'
        })
    else:
        # prepare data to return
        data = {'spgiohang': list(spgiohang)}
        # return JSON
        return JsonResponse(data)
    

@login_required
def LaySlSpGioHang(request):
    try:
        # find todo by id
        spgiohang = GioHang.objects.all().filter(user_id = request.user.id)
    except ObjectDoesNotExist:
        # return 404 if the todo does not exists
        return JsonResponse({
            'status_code': 404,
            'error': f'Todo with id {pk} not found.'
        })
    else:
        # prepare data to return
        data = {'sl': len(list(spgiohang.values()))}
        # return JSON
        return JsonResponse(data)



@login_required
@csrf_exempt 
def ThemSpGiohang(request):
    if request.method == 'POST':
      try:
          body = json.loads(request.body.decode("utf-8"))
          userId = int(body['userId'])
          kichcosanphamId = int(body['kichcosanphamId'])
          soluong = int(body['soluong'])
          sp = GioHang.objects.filter(Q(user__id=request.user.id), Q(kichcosanpham__id=kichcosanphamId)).first();
          if(sp):
              sp.soluong = soluong;
              sp.ngaythem = timezone.now();
              sp.save();
          else:
              themSp = GioHang.objects.create(
                  soluong=soluong,
                  kichcosanpham_id=kichcosanphamId,
                  user_id=userId,
              )
              themSp.save()
      except ObjectDoesNotExist:
          # return 404 if the todo does not exists
          return JsonResponse({
              'status_code': 404,
              'error': f'Todo with id {1} not found.'
          })
      else:
          # prepare data to return
          data = {'data': True}
          # return JSON
          return JsonResponse(data)
      

@login_required
@csrf_exempt 
def DiaChiNguoiDung(request, pk):
    x = 1
    if request.method == 'GET':
        try:
            dsdiachi = DiaChi.objects.all().filter(user__id = pk).order_by("-macdinh")
        except ObjectDoesNotExist:
            # return 404 if the todo does not exists
            return JsonResponse({
                'status_code': 404,
                'error': f'Id {pk} not found.'
            })
        else:
            # prepare data to return
            data = {'dsdiachi': list(dsdiachi.values())}
            # return JSON
            return JsonResponse(data)
    elif request.method == 'POST':
        try:
          body = json.loads(request.body.decode("utf-8"))
          isRemove = bool(body['isRemove']);
          if isRemove:
            diachiId = body['id']
            DiaChi.objects.filter(id=diachiId).delete()
          else: 
            sdt = body['sdt']
            diachi = body['diachi']
            diachicuthe = body['diachicuthe']
            macdinh = body['macdinh']
            isUpdate = bool(body['isUpdate'])
            userId = int(body['userId'])

            if(isUpdate):
                if macdinh == True:
                    DiaChi.objects.filter(user_id=userId).update(macdinh=False)
                diachiId = body['id']
                dc = DiaChi.objects.filter(Q(id=diachiId)).first();
                dc.sdt = sdt
                dc.diachi = diachi
                dc.diachicuthe = diachicuthe
                dc.macdinh = macdinh
                dc.save()
            else:
                if macdinh == True:
                    DiaChi.objects.filter(user_id=userId).update(macdinh=False)
                themDiaChi = DiaChi.objects.create(
                    sdt=sdt,
                    diachi=diachi,
                    diachicuthe=diachicuthe,
                    macdinh=macdinh,
                    user_id=userId
                )
                themDiaChi.save()
        except ObjectDoesNotExist:
            # return 404 if the todo does not exists
            return JsonResponse({
                'status_code': 404,
                'error': f'Todo with id {1} not found.'
            })
        else:
            # prepare data to return
            data = {'data': True}
            # return JSON
            return JsonResponse(data)


@login_required
@csrf_exempt 
def GioHangNguoiDung(request):
    if request.method == 'POST':
        try:
          body = json.loads(request.body.decode("utf-8"))
          loai = str(body['type']);
          kichcosanpham_id = body['id']
          if loai == "capnhat":
              hd = str(body['event'])
              gt = 1 if hd == "tang" else (-1)

              kichcosanpham_ = KichCoSanPham.objects.get(pk=kichcosanpham_id)
              chitietgiohang_ = GioHang.objects.filter(Q(kichcosanpham_id=kichcosanpham_id), Q(user_id=request.user.id)).first()

              hd = str(body['event'])
              if hd == "tang":
                  if(int(kichcosanpham_.soluong) > int(chitietgiohang_.soluong)):
                      GioHang.objects.filter(Q(kichcosanpham_id=kichcosanpham_id)).update(soluong=F('soluong') + (gt))
                  else:
                      return JsonResponse({'data': False})
              else: 
                  GioHang.objects.filter(Q(kichcosanpham_id=kichcosanpham_id)).update(soluong=F('soluong') + (gt))
          else:
              GioHang.objects.filter(kichcosanpham_id=kichcosanpham_id).delete()
        except ObjectDoesNotExist:
            # return 404 if the todo does not exists
            return JsonResponse({
                'status_code': 404,
                'error': f'Todo with id {1} not found.'
            })
        else:
            # prepare data to return
            data = {'data': True}
            # return JSON
            return JsonResponse(data)



@login_required
def LayDsDonHang(request, trangthaiId):
    try:
        loaiSx = "";
        if int(trangthaiId) == 1:
            loaiSx = "-ngaytaoo"
        else:
            loaiSx = "-ngaysuaa"
        dsdonhang = DonHang.objects.select_related('chitietdonhang__kichcosanpham__loaisanpham__sanpham').filter(trangthaidonhang_id=trangthaiId, user_id=request.user.id).values(
        idd=F('id'),
        chitietdonhang_id=F('chitietdonhang__id'),
        TrangThaiDonHang_id=F('trangthaidonhang_id'),
        tongtienn=F('tongtien'),
        ngaytaoo=F('ngaytao'),
        ngaysuaa=F('ngaysua'),
        gia=F('chitietdonhang__gia'),
        soluongg=F('chitietdonhang__soluong'),
        SanPham_id=F('chitietdonhang__kichcosanpham__loaisanpham__sanpham__id'),
        KichCoSanPham_id=F('chitietdonhang__kichcosanpham__id'),
        ten=F('chitietdonhang__kichcosanpham__loaisanpham__sanpham__ten'),
        mausac=F('chitietdonhang__kichcosanpham__loaisanpham__mausac'),
        hinhanh=F('chitietdonhang__kichcosanpham__loaisanpham__hinhanh'),
        kichco=F('chitietdonhang__kichcosanpham__kichco'),
        ).order_by("-ngaytaoo")
        for donhang in dsdonhang:
            donhang['ngaytaoo'] = donhang['ngaytaoo'].strftime('%Y-%m-%d %H-%M-%S')
            if donhang['ngaysuaa']:
                donhang['ngaysuaa'] = donhang['ngaysuaa'].strftime('%Y-%m-%d %H-%M-%S')
    except ObjectDoesNotExist:
        return JsonResponse({
            'status_code': 404,
            'error': f'Todo with id {11} not found.'
        })
    else:
        # prepare data to return
        data = {'dsdonhang': list(dsdonhang)}
        # return JSON
        return JsonResponse(data)
    

@login_required
@csrf_exempt 
def DanhGiaSpDonHang(request):
    if request.method == 'POST':
      try:
          body = json.loads(request.body.decode("utf-8"))

            # 'arrId' => $decode['orderId'],
            #     "sosao" => $decode['star'],
            #     "binhluan" => $decode['mes'],


          userId = int(body['userId'])
          kichcosanphamId = int(body['kichcosanphamId'])
          soluong = int(body['soluong'])
          sp = GioHang.objects.filter(Q(user__id=userId), Q(kichcosanpham__id=kichcosanphamId)).first();
          if(sp):
              sp.soluong = soluong;
              sp.ngaythem = timezone.now();
              sp.save();
          else:
              themSp = GioHang.objects.create(
                  soluong=soluong,
                  kichcosanpham_id=kichcosanphamId,
                  user_id=userId,
              )
              themSp.save()
      except ObjectDoesNotExist:
          # return 404 if the todo does not exists
          return JsonResponse({
              'status_code': 404,
              'error': f'Todo with id {1} not found.'
          })
      else:
          # prepare data to return
          data = {'data': True}
          # return JSON
          return JsonResponse(data)

@login_required
@csrf_exempt 
def HuyDonHang(request):
    if request.method == 'POST':
        try:
          body = json.loads(request.body.decode("utf-8"))
          dhid = str(body['dhId']);

          dc = DonHang.objects.filter(Q(id=dhid)).first();
          dc.trangthaidonhang_id = 4
          dc.ngaysua = timezone.now()
          dc.save()
        except ObjectDoesNotExist:
            # return 404 if the todo does not exists
            return JsonResponse({
                'status_code': 404,
                'error': f'Todo with id {1} not found.'
            })
        else:
            # prepare data to return
            data = {'data': True}
            # return JSON
            return JsonResponse(data)
        


@login_required
def LayDonHangId(request, iddh):
    try:
        iddd = iddh
        dsdonhang = DonHang.objects.select_related('thongtindonhang','chitietdonhang__kichcosanpham__loaisanpham__sanpham').filter(id=iddh).values(
        idd=F('id'),
        TrangThaiDonHang_id=F('trangthaidonhang_id'),
        tongtienn=F('tongtien'),
        ngaytaoo=F('ngaytao'),
        ngaysuaa=F('ngaysua'),
        gia=F('chitietdonhang__gia'),
        soluongg=F('chitietdonhang__soluong'),
        SanPham_id=F('chitietdonhang__kichcosanpham__loaisanpham__sanpham__id'),
        KichCoSanPham_id=F('chitietdonhang__kichcosanpham__id'),
        ten=F('chitietdonhang__kichcosanpham__loaisanpham__sanpham__ten'),
        mausac=F('chitietdonhang__kichcosanpham__loaisanpham__mausac'),
        hinhanh=F('chitietdonhang__kichcosanpham__loaisanpham__hinhanh'),
        kichco=F('chitietdonhang__kichcosanpham__kichco'),
        diachii=F('thongtindonhang__diachinhanhang'),
        sdtt=F('thongtindonhang__sdt'),
        ).all()
    except ObjectDoesNotExist:
        return JsonResponse({
            'status_code': 404,
            'error': f'Todo with id {11} not found.'
        })
    else:
        # prepare data to return
        data = {'dsdonhang': list(dsdonhang)}
        # return JSON
        return JsonResponse(data)