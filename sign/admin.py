from django.contrib import admin
from sign.models import Event, Guest

# Register your models here.
# 通知admin管理工具未这些模块逐一提供洁面


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'limit', 'status', 'address', 'start_time']
    # 创建表字典的搜索器
    search_fields = ['name']
    # 创建字段过滤器
    list_filter = ['status']


class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event']
    search_fields = ['realname', 'phone']
    list_filter = ['sign']


admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)

# e1 = Event(id=2, name='红米Pro发布会', limit=2000, status=True, address='北京', start_time=datetime(2016,8,10,14,0,0))
