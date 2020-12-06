from rest_framework import serializers  # 시리얼라이저는 api를 만들때 폼이 해주는 역할을 함
from .models import Sproduct


class ProductSerializer(serializers.ModelSerializer):

    # 모델 가져오기 fields all로 하면 모든 필드를 가져옴
    class Meta:
        model = Sproduct
        fields = '__all__'
