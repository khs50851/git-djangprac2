from django.db import models

# Create your models here.


class Suser(models.Model):
    email = models.EmailField(verbose_name='이메일')
    password = models.CharField(max_length=128, verbose_name='비밀번호')
    level = models.CharField(max_length=8, verbose_name='등급',
                             choices=(
                                 # 초이스는 레벨에 들어갈 수 있는 값을 미리 정함
                                 ('admin', '관리자'),
                                 ('user', '유저')
                             ))
    regdate = models.DateTimeField(auto_now_add=True, verbose_name='등록일')

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'db_user'
        verbose_name = '유저'
        verbose_name_plural = '유저'  # 이건 복수형
