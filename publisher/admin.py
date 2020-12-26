from django.contrib import admin

# Register your models here.
from publisher.models import Product

admin.site.register(Product)

# 校园小商品后台管理系统
admin.site.site_header = '校园小商品后台管理系统'
