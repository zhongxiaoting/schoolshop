from PIL import Image
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.utils import timezone


class Product(models.Model):
    # 发布者,外键方式删除
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    # 联系方式
    phone = models.CharField(max_length=20, blank=False)
    # 图片
    avatar = models.ImageField(upload_to='images/%Y%m%d/', blank=True)
    # 商品名称
    name = models.CharField(max_length=50)
    # 商品价格
    price = models.CharField(max_length=20)
    # 商品销售量
    total_sale = models.PositiveIntegerField(default=0)
    # 商品描述
    description = models.TextField()
    # 商品的发布时间
    created = models.DateTimeField(default=timezone.now)

    # 保存图片
    def save(self, *args, **kwargs):
        images = super(Product, self).save(*args, **kwargs)
        # 缩放图片
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 350
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return images

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name
