from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Sproduct
from .forms import RegisterForm
# Create your views here.


class ProductList(ListView):
    model = Sproduct
    template_name = 'product.html'
    context_object_name = 'product_list'  # object_list 이걸 바꾸는거


class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'


class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Sproduct.objects.all()  # 어떤 모델이 아니라 쿼리셋을 지정해서 넣어야함
    # 조건 지정시 필터로 조건 지정할수있음
    print("쿼리셋 : ", queryset)
    context_object_name = 'product'
