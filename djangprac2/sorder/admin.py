from django.contrib import admin
from django.utils.html import format_html
from .models import Sorder

# Register your models here.


class SorderAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    # 스타일된 스테이터스를 함수로 만들수있음
    list_display = ('suser', 'product', 'styled_status')

    def styled_status(self, obj):  # 이 함수를 만들고 등록 obj는 각 레코드를 의미
        if obj.status == '환불':
            return format_html(f'<span style="color:red;font-weight:bold">{obj.status}</span>')
        if obj.status == '결제완료':
            return format_html(f'<span style="color:green;font-weight:bold">{obj.status}</span>')
        return obj.status

    # 함수를 만들면 함수에 대한 속성값을 지정할 수 있음
    styled_status.short_description = '상태'  # 위에도 styled_status이게 아니라 상태로 나오게함


admin.site.register(Sorder, SorderAdmin)
