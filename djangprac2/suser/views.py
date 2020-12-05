from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import RegisterForm
# Create your views here.


def index(request):
    return render(request, 'index.html')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'  # 저장 성공시 가는 url
