from django.contrib import admin
from .models import Sorder
# Register your models here.


class SorderAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    # 스타일된 스테이터스를 함수로 만들수있음
    list_display = ('suser', 'product', 'styled_status')

    def styled_status(self, obj):  # 이 함수를 만들고 등록 obj는 각 레코드를 의미
        return obj.status


admin.site.register(Sorder, SorderAdmin)
