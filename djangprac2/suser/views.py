from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
# Create your views here.


def index(request):
    return render(request, 'index.html', {'email': request.session.get('user')})


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'  # 저장 성공시 가는 url


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'  # 저장 성공시 가는 url

    def form_valid(self, form):  # 이 함수는 유효성 검사가 끝나고 모든 데이터가 정상적일때
        self.request.session['user'] = form.email

        return super().form_valid(form)
