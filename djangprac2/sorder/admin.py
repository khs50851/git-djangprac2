from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
import datetime
from django.db import transaction
from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.urls import path
from .models import Sorder

# Register your models here.


def refund(modeladmin, request, queryset):  # 이 함수를 밑에 등록 그럼 액션즈에 등록된 함수 안에 3개의 인자값을 전달

    # 여러 모델에 한번에 변경을 하는것이므로 트랜잭션해야함 조회부터 트랜잭션 안에 있어야함
    with transaction.atomic():
        # 쿼리셋에서 필터를 걸어서 또 sub set을 만들수있음 Q를 통해 not을 만들수 있음 ~Q하면 not 의 의미
        qs = queryset.filter(~Q(status='환불'))  # 환불이 아닌거만 쿼리셋으로 가져오는거
        ct = ContentType.objects.get_for_model(
            queryset.model)  # 모델을 얻고 쿼리셋 안에 무슨 모델인지 들어있음
        for obj in qs:  # obj는 모델로 온거 이렇게하면 환불계속하면 계속 늘어남 환불이 되어있는 경우를 제외해야함
            obj.product.stock += obj.quantity
            obj.product.save()

            # 액션을 추가하면 로그엔트리에 추가됨
            LogEntry.objects.log_action(  # 스태틱 함수임 그래서 log_action이라는 함수 그대로 사용하면됨
                user_id=request.user.id,  # 백오피스에서 쓰는 유저아이디
                # 로그 엔트리는 모델에 관계없이 쓰임 그래서 무슨 모델을 받니? 라는걸 물어봄 그떄 사용하는게 contenttype
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr='주문 환불',
                action_flag=CHANGE,  # 추가인지 삭제인지 알려줌
                change_message='주문 환불'

            )  # 어떤 동작

        qs.update(status='환불')  # F는 디비에 저장된 값을 변경할떄 씀 상태를 환불로 변경함


refund.short_description = '환불'


class SorderAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    # 스타일된 스테이터스를 함수로 만들수있음
    list_display = ('suser', 'product', 'styled_status', 'action')

    # 어드민파일에서 내가 만든 html파일을 지정해줄수있음
    change_list_template = 'admin/order_change_list.html'  # 이렇게 템플릿 파일의 경로 지정
    change_form_template = 'admin/order_change_form.html'

    actions = [  # 안에다가 함수를 넣음
        refund  # 함수 호출
    ]

    def action(self, obj):
        if obj.status != '환불':
            return format_html(f'<input type="button" value="환불" onclick="order_refund_submit({obj.id})" class="btn btn-primary btn-sm"></button>')

    def styled_status(self, obj):  # 이 함수를 만들고 등록 obj는 각 레코드를 의미
        if obj.status == '환불':
            return format_html(f'<span style="color:red;font-weight:bold">{obj.status}</span>')
        if obj.status == '결제완료':
            return format_html(f'<span style="color:green;font-weight:bold">{obj.status}</span>')
        return obj.status

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': '주문 목록'}

        if request.method == 'POST':
            obj_id = request.POST.get('obj_id')
            if obj_id:
                qs = Sorder.objects.filter(pk=obj_id)

                ct = ContentType.objects.get_for_model(qs.model)

                for obj in qs:
                    obj.product.stock += obj.quantity
                    obj.product.save()

                    LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ct.pk,
                        object_id=obj.pk,
                        object_repr='주문환불',
                        action_flag=CHANGE,
                        change_message='주문환불'
                    )
                qs.update(status='환불')
        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        sorder = Sorder.objects.get(pk=object_id)
        extra_context = {
            'title': f'{sorder.suser.email}의{sorder.product.name} 주문 수정하기'}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_add_continue'] = False
        return super()._changeform_view(request, object_id, form_url, extra_context)

    def date_view(self, request):  # 새로운 뷰는 만들어졌는데 이거에 맞는 템플릿 파일을 만들어야함
        week_date = datetime.datetime.now()-datetime.timedelta(days=7)  # 7일을 뺌
        week_data = Sorder.objects.filter(regdate__gte=week_date)
        data = Sorder.objects.filter(regdate__lt=week_date)
        context = dict(
            self.admin_site.each_context(request),  # 이렇게 채워줘야함
            week_data=week_data,
            data=data
        )
        # context에 기본적인게 없어서 원래것보다 비어서 전달됨
        return TemplateResponse(request, 'admin/order_date_view.html', context)
        # 함수를 만들면 함수에 대한 속성값을 지정할 수 있음

    # 주소를 추가하자
    def get_urls(self):
        urls = super().get_urls()
        date_urls = [  # 새로 추가할 url
            path('date_view/', self.date_view),
        ]
        return date_urls+urls  # 기존에 생성된 urls랑 내가만든 date_urls 반환
    styled_status.short_description = '상태'  # 위에도 styled_status이게 아니라 상태로 나오게함


admin.site.register(Sorder, SorderAdmin)
