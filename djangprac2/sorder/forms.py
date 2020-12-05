from django import forms
from .models import Sorder
from sproduct.models import Sproduct
from suser.models import Suser
from django.db import transaction


class RegisterForm(forms.Form):

    # 생성자 함수를 만들면서 request를 전달할수있게 인터페이스를 만들고 폼뷰랑 폼을 생성할때 이 리퀘를 전달할수 있게함
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(
        error_messages={
            'required': '수량을 입력하세요'
        }, label='수량'
    )
    product = forms.IntegerField(  # 상품 id로해서 상품정보를 넘겨받음
        error_messages={
            'required': '상품설명을 입력하세요'
        }, label='상품설명', widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        suser = self.request.session.get('user')

        if quantity and product and suser:
            with transaction.atomic():
                prod = Sproduct.objects.get(pk=product)
                sorder = Sorder(
                    # 참조키이기때문에 그 모델을 임포트 해야함
                    quantity=quantity,
                    product=prod,
                    suser=Suser.objects.get(email=suser)
                )
            print("product121212 : ", product)
            sorder.save()
            prod.stock -= quantity
            prod.save()

            # atomic안에서 발생되는 일들은 트랜잭션으로 처리됨

        else:
            self.product = product
            self.add_error('quantity', '값이 없습니다.')
            self.add_error('product', '값이 없습니다.')

# 트랜잭션으로 만들겠다라는것은
# 일련의 동작을 하나로 만들겠다
# 전체가 다 성공하면 성공이고 그중에 하나라도 실패하면
# 롤백으로 다시 되돌림
# 주문하기같은경우 주문(하나의 동작) 그리고 상품의 재고도 줄어야함
# 동시에 이루어져야하고 하나라도 안되면 그냥 실패로 롤백
