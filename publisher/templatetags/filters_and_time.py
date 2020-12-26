from django import template

from django.utils import timezone
import math

register = template.Library()


@register.filter(name='transfer')
def transfer(value, arg):
    """将输出强制转换为字符串 arg """
    return arg


@register.filter()
def lower(value):
    """将字符串转换为小写字符"""
    return value.lower()


# 获取相对时间
@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and 0 <= diff.seconds < 60:
        return '刚刚'

    if diff.days == 0 and 60 <= diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分钟前"

    if diff.days == 0 and 3600 <= diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if 1 <= diff.days < 30:
        return str(diff.days) + "天前"

    if 30 <= diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"
