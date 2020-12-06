from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.db import transaction
from .models import Sorder
from .forms import RegisterForm
from suser.decorators import login_required
from sproduct.models import Sproduct
from suser.models import Suser
# Create your views here.


@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = "/product/"

    def form_valid(self, form):
        with transaction.atomic():
            prod = Sproduct.objects.get(pk=form.data.get('product'))
            sorder = Sorder(
                # 참조키이기때문에 그 모델을 임포트 해야함
                quantity=form.data.get('quantity'),
                product=prod,
                suser=Suser.objects.get(email=self.request.session.get('user'))
            )
            sorder.save()
            prod.stock -= int(form.data.get('quantity'))
            prod.save()

        return super().form_valid(form)
    # 실패했을경우 다시 상품 상세보기페이지로 들어오게

    def form_invalid(self, form):
        return redirect('/product/'+str(form.data.get('product')))

    def get_form_kwargs(self, **kwargs):  # 폼을 생성할때 어떤 인자값을 전달해서 만들건지를 결정하는 함수
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw
    # 리퀘스트라는 변수를 전달할 수 있게 만들어야함


# url에 접근했을때 클래스를 호출해주는 함수는 dispatch임
@ method_decorator(login_required, name='dispatch')
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
