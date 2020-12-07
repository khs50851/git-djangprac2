from django.contrib import admin
from .models import Suser
# Register your models here.


class SuserAdmin(admin.ModelAdmin):
    list_display = ('email',)  # 뒤에 콤마를 꼭 써야함 안그럼 튜플로 인식을 안함 문자열로 인식


admin.site.register(Suser, SuserAdmin)
admin.site.site_header = 'HS쇼핑몰'  # 어드민 사이트 이름 변경(왼쪽 상단)
admin.site.index_title = 'HS쇼핑몰3'
admin.site.site_title = 'HS쇼핑몰2'
