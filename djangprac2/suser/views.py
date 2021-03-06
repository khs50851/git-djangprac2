from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import check_password, make_password
from .forms import RegisterForm, LoginForm
from .models import Suser
# Create your views here.


def index(request):
    return render(request, 'index.html', {'email': request.session.get('user')})


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'  # 저장 성공시 가는 url

    def form_valid(self, form):  # 유효성 검사가 끝나고 호출되는 함수
        suser = Suser(
            email=form.data.get('email'),  # 폼안에 데이터를 가져옴
            password=make_password(form.data.get('password')),
            level='user'
        )
        suser.save()
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'  # 저장 성공시 가는 url

    def form_valid(self, form):  # 이 함수는 유효성 검사가 끝나고 모든 데이터가 정상적일때
        self.request.session['user'] = form.data.get('email')

        return super().form_valid(form)


def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')
