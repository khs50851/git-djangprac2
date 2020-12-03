from django.contrib import admin
from .models import Suser
# Register your models here.


class SuserAdmin(admin.ModelAdmin):
    list_display = ('email',)  # 뒤에 콤마를 꼭 써야함 안그럼 튜플로 인식을 안함 문자열로 인식


admin.site.register(Suser, SuserAdmin)
