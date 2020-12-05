from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
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
