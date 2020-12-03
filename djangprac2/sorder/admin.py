from django.contrib import admin
from .models import Sorder
# Register your models here.


class SorderAdmin(admin.ModelAdmin):
    list_display = ('suser', 'product')


admin.site.register(Sorder, SorderAdmin)
