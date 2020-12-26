from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView

from userprofile.models import Profile
from .forms import productForm
from publisher.models import Product
# 引入Q对象
from django.db.models import Q


def publisher_list(request):
    # 搜索商品
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        product_list = Product.objects.filter(Q(price__contains=search) | Q(name__contains=search))
        print(product_list)
    else:
        search = ''
        product_list = Product.objects.all()
    if order == 'price':
        product_list = product_list.order_by('-price')
    else:
        pass
    paginator = Paginator(product_list, 3)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    # 传递给模板的对象
    context = {'products': products, 'search': search, 'order': order}
    # 载入模板，返回给context
    return render(request, 'publisher/list.html', context)


# 详情页面
def publisher_detail(request, id):
    # 取出相应的商品
    products = Product.objects.get(id=id)
    profile = Profile.objects.all()
    # 传递给模板
    context = {'products': products, 'profile': profile}
    # 载入模板，返回给context
    return render(request, 'publisher/detail.html', context)


# 新增商品信息
@login_required(login_url='profile/login/')
def publisher_create(request):
    # 判断是否提交
    if request.method == 'POST':
        product_post_form = productForm(request.POST, request.FILES)
        if product_post_form.is_valid():
            new_product = product_post_form.save(commit=False)
            new_product.publisher = User.objects.get(id=request.user.id)
            new_product.save()
            return redirect('publisher:publisher_list')
        else:
            return HttpResponse('表单有误，重新填写')
    else:
        product_post_form = productForm()
        context = {'product_post_form': product_post_form}
        return render(request, 'publisher/create.html', context)


# 删除商品
def publisher_safe_delete(request, id):
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('publisher:publisher_list')
    else:
        return HttpResponse("仅允许POST请求")


# 修改商品
def publisher_update(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product_post_form = productForm(data=request.POST)
        if product_post_form.is_valid():
            product.name = request.POST['name']
            product.price = request.POST['price']
            product.description = request.POST['description']
            if request.FILES.get('avatar'):
                product.avatar = request.FILES.get('avatar')
            product.save()
            return redirect('publisher:publisher_detail', id=id)
        else:
            return HttpResponse("输入的表单有误，请重新输入")
    # GET提交
    else:
        product_post_form = productForm()
        context = {'products': product, 'product_post_form': product_post_form}
        return render(request, 'publisher/update.html', context)


# 出售量
class publisher_sale(View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs.get('id'))
        product.total_sale += 1
        product.save()
        return HttpResponse('success')
