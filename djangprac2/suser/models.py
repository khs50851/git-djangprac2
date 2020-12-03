from django.db import models

# Create your models here.


class Suser(models.Model):
    email = models.EmailField(verbose_name='이메일')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    regdate = models.DateTimeField(auto_now_add=True, verbose_name='등록일')

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'db_user'
        verbose_name = '유저'
        verbose_name_plural = '유저'  # 이건 복수형
