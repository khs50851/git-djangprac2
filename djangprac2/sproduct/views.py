from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework import mixins
from .serializers import ProductSerializer

from .models import Sproduct
from .forms import RegisterForm
from sorder.forms import RegisterForm as SorderForm
from suser.decorators import admin_required
# Create your views here.

# rest를 이용한 뷰


class ProductListAIP(generics.GenericAPIView, mixins.ListModelMixin):  # mixin은 하나의 컴포넌트
    # 만약 이 클래스뷰안에서 get메소드와 post메소드를 제공할건데
    # get에서는 list형태의 api만들고싶고 post는 생성에 대한 api를 만들고싶다?
    # 두가지 기능중에 get에 대한 mixin 클래스를 가져와 상속
    # post에 mixin 클래스를 가져와 상속받음

    # 어떤 데이터를 가지고할지 명시해야함 앞에서 만든 시리얼라이저랑 쿼리셋으로 지정해서 명시

    serializer_class = ProductSerializer  # 데이터에대한 검증을 해야해서 시리얼라이저를 등록함

    def get_queryset(self):
        return Sproduct.objects.all().order_by('id')  # 데이터 가져옴

    def get(self, request, *args, **kwargs):  # 저 믹스인 안에 함수가 만들어져있음 겟함수안에서 리스트를 호출함
        return self.list(request, *args, **kwargs)


# mixin은 하나의 컴포넌트 # 상세페이지를 위한 mixin
class ProductDetailAIP(generics.GenericAPIView, mixins.RetrieveModelMixin):

    serializer_class = ProductSerializer  # 데이터에대한 검증을 해야해서 시리얼라이저를 등록함

    def get_queryset(self):
        # 왜 상세보기인데 all이냐?
        return Sproduct.objects.all().order_by('id')  # 데이터 가져옴
    # 이 믹스인을 상속받고 겟을 사용하면 url에서 pk값을 연결해줘야함
    # 그럼 이 쿼리셋 안에서 해당 pk를 가지고있는 상품만 꺼내서 줌

    def get(self, request, *args, **kwargs):  # 저 믹스인 안에 함수가 만들어져있음 겟함수안에서 리스트를 호출함
        return self.retrieve(request, *args, **kwargs)


class ProductList(ListView):
    model = Sproduct
    queryset = Sproduct.objects.all().order_by('-id')
    template_name = 'product.html'
    context_object_name = 'product_list'  # object_list 이걸 바꾸는거


@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        product = Sproduct(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stock=form.data.get('stock')
        )
        product.save()
        return super().form_valid(form)


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
