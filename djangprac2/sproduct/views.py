from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Sproduct
from .forms import RegisterForm
from sorder.forms import RegisterForm as SorderForm
# Create your views here.


class ProductList(ListView):
    model = Sproduct
    queryset = Sproduct.objects.all().order_by('-id')
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

# 디테일 뷰에서 만든 폼을 받을게 없어서 만들어야함
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # super()를 통해 기존에 호출되는 함수를 먼저 호출
        # 그러니까 먼저 디테일 뷰가 자동으로 전달해주는 데이터를 먼저 만들고
        context['form'] = SorderForm(self.request)
        # 폼을 생성할때 셀프에 있는 리퀘스트
        # 여기는 뷰클래스이기 때문에 셀프안에 리퀘스트가 있음
        return context

        # 먼저 생성된 context안에 form이라는 하나의 데이터를 추가했고 그걸 반환
