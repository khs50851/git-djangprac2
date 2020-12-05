from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .models import Sorder
from .forms import RegisterForm

# Create your views here.


class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = "/product/"

    # 실패했을경우 다시 상품 상세보기페이지로 들어오게
    def form_invalid(self, form):
        return redirect('/product/'+str(form.product))

    def get_form_kwargs(self, **kwargs):  # 폼을 생성할때 어떤 인자값을 전달해서 만들건지를 결정하는 함수
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw
    # 리퀘스트라는 변수를 전달할 수 있게 만들어야함


class OrderList(ListView):
    model = Sorder  # 그냥 모델로만 하면 전체 회원의 주문목록이 나옴
    # 세션으로 사용자 정보를 받아와야함

    template_name = 'order.html'
    context_object_name = 'order_list'

    # 쿼리셋 오버라이딩하자
    def get_queryset(self, **kwargs):
        queryset = Sorder.objects.filter(
            suser__email=self.request.session.get('user'))
        # suser__email은 suser의 email이 세션값인거
        return queryset
