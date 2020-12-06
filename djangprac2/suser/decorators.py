from django.shortcuts import redirect
from .models import Suser
# 등록을 해야하는데 로그인이 되어있을경우만 등록 가능하게 만들어야함


def login_required(function):
    # dispatch 함수는 기본 인자값을 갖고있는데 wrap함수에 아무것도 없으면 에러남 그래서 인자값을 맞춰줘야함
    def wrap(request, *args, **kwargs):
        suser = request.session.get('user')
        if suser is None or not suser:
            return redirect('/login')

        return function(request, *args, **kwargs)

    return wrap


def admin_required(function):
    def wrap(request, *args, **kwargs):
        suser = request.session.get('user')
        if suser is None or not suser:
            return redirect('/login')

        suser = Suser.objects.get(email=suser)
        if suser.level != 'admin':
            return redirect('/')

        return function(request, *args, **kwargs)

    return wrap
