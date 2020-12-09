"""djangprac2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import datetime
from django.contrib import admin

from django.template.response import TemplateResponse
from django.urls import path, include, re_path
from suser.views import index, RegisterView, LoginView, logout
from sproduct.views import ProductList, ProductCreate, ProductDetail, ProductListAIP, ProductDetailAIP
from sorder.views import OrderCreate, OrderList
from django.views.generic import TemplateView
from sorder.models import Sorder
from .functions import get_exchange
orig_index = admin.site.index  # 함수를 변수에 담을 수 있음


def hsindex(request, extra_context=None):
    base_date = datetime.datetime.now() - datetime.timedelta(days=7)
    order_date = {}
    for i in range(7):
        target_dttm = base_date + datetime.timedelta(days=i)
        date_key = target_dttm.strftime('%Y-%m-%d')
        target_date = datetime.date(
            target_dttm.year, target_dttm.month, target_dttm.day)
        order_cnt = Sorder.objects.filter(
            regdate__date=target_date).count()  # 그 날짜에 대한 주문건수

        order_date[date_key] = order_cnt
    extra_context = {
        'orders': order_date,
        'exchange': get_exchange()
    }
    return orig_index(request, extra_context)  # 이렇게하면 데이터를 끼워 넣을수있음


admin.site.index = hsindex

urlpatterns = [
    re_path(r'^admin/manual/$', TemplateView.as_view(template_name='admin/manual.html',  # admin/ 위에다가 써야함 re_path는 정확히 저거랑 일치할때 보내겠다 ^는 시작 $는 끝을 의미
                                                     extra_context={'title': '매뉴얼', 'site_title': 'HS', 'site_header': 'HS'})),

    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('', index),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
    path('product/', ProductList.as_view()),
    path('product/create/', ProductCreate.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('order/create/', OrderCreate.as_view()),
    path('order/', OrderList.as_view()),
    path('api/product/', ProductListAIP.as_view()),
    path('api/product/<int:pk>/', ProductDetailAIP.as_view()),

]
