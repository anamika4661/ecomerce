from django.contrib import admin
from .models import *
from csvexport.actions import csvexport
# Register your models here.
class itemi(admin.ModelAdmin):
    list_display = ("title","price","image")
    search_fields = ["title","description"]
    list_filter = ("status","label","category")
    list_per_page = 2
    actions = [csvexport]

admin.site.register(item,itemi)

class categoryadmin(admin.ModelAdmin):
    list_display = ("name","slug","image")
    search_fields = ["name"]
    list_per_page = 2

admin.site.register(category,categoryadmin)

admin.site.register(slider)
admin.site.register(ad)
admin.site.register(brand)
admin.site.register(cart)
admin.site.register(contact)