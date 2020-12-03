from django.contrib import admin
from .models import Sproduct
# Register your models here.


class SproductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


admin.site.register(Sproduct, SproductAdmin)
