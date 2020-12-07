from django.contrib import admin
from .models import Suser
# Register your models here.


class SuserAdmin(admin.ModelAdmin):
    list_display = ('email',)  # 뒤에 콤마를 꼭 써야함 안그럼 튜플로 인식을 안함 문자열로 인식

    # suseradmin 클래스 만들면서(어드민페이지에 접속할때) 이 함수를 자동으로 호출함
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': '사용자목록'}  # 위쪽에 Select 사용자 to change 이거 바꾸는거
        # 우리가 원하는 동작을 하고 아래 return문 실행됨 위에 구문을 끼워 넣어준셈
        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        suser = Suser.objects.get(pk=object_id)
        extra_context = {'title': f'{suser.email} 수정하기'}
        return super()._changeform_view(request, object_id, form_url, extra_context)


admin.site.register(Suser, SuserAdmin)
admin.site.site_header = 'HS쇼핑몰'  # 어드민 사이트 이름 변경(왼쪽 상단)
admin.site.index_title = 'HS쇼핑몰3'
admin.site.site_title = 'HS쇼핑몰2'
