from django.db import models

# Create your models here.


class Sorder(models.Model):
    suser = models.ForeignKey(
        'suser.Suser', on_delete=models.CASCADE, verbose_name='유저')
    product = models.ForeignKey(
        'sproduct.Sproduct', on_delete=models.CASCADE, verbose_name='상품')
    quantity = models.IntegerField(verbose_name='수량')
    regdate = models.DateTimeField(auto_now_add=True, verbose_name='등록일')

    def __str__(self):  # admin에서 ~~.object라고 나오는걸 구체적으로 바꿈
        return str(self.suser)+' '+str(self.product)

    class Meta:
        db_table = 'db_order'
        verbose_name = '주문'
        verbose_name_plural = '주문'  # 이건 복수형
