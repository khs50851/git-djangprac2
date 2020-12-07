from django.contrib import admin
from django.utils.html import format_html
# 이거 휴머나이즈 가져오려면 settings에 앱 추가 해야함
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Sproduct

# Register your models here.


class SproductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_format', 'styled_stock')

    def price_format(self, obj):
        price = intcomma(obj.price)
        return f'{price} 원'

    def styled_stock(self, obj):  # 이 함수를 만들고 등록 obj는 각 레코드를 의미
        stock = obj.stock

        if stock <= 50:
            stock = intcomma(stock)
            return format_html(f'<b><span style="color:red;font-weight:bold">{stock} 개</span></b>')
        return f'{intcomma(stock)} 개'  # f스트링 안에 함수도 쓸수있음
    price_format.short_description = '가격'
    styled_stock.short_description = '재고'


admin.site.register(Sproduct, SproductAdmin)
