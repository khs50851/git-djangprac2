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

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': '상품 목록'}
        return super().changelist_view(request, extra_context)

    # 상세보기가면 위에 나타나는 제목수정
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        product = Sproduct.objects.get(pk=object_id)
        extra_context = {'title': f'{product.name} 수정하기'}
        return super().changeform_view(request, object_id, form_url, extra_context)
    price_format.short_description = '가격'
    styled_stock.short_description = '재고'


admin.site.register(Sproduct, SproductAdmin)
