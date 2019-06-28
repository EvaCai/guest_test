# coding=utf-8
from django.conf.urls import url
from django.urls import path
from sign import view_if, view_if_sec

urlpatterns = [
    # sign system interface:
    # ex: /api/add_event/
    url(r'^add_event/$', view_if.add_event, name='add_event'),
    # ex: /api/add_guest/
    url(r'add_guest/', view_if.add_guest, name='add_guest'),
    # ex: /api/get_event_list
    url(r'^get_event_list/$', view_if.get_event_list, name='get_event_list'),
    # ex: /api/get_guest_list/
    url(r'get_guest_list/', view_if.get_guest_list, name='get_guest_list'),
    # ex: /api/user_sign/
    url(r'user_sign/', view_if.user_sign, name='user_sign'),

    url(r'^sec_get_event_list/$', view_if_sec.sec_get_event_list, name='sec_get_event_list'),
    url(r'sign_add_event/', view_if_sec.sign_add_event, neme='sign_add_event'),


    # path('add_event/', view_if.add_event),
    # # ex: /api/add_guest/
    # path('add_guest/', view_if.add_guest),
    # # ex: /api/get_event_list
    # path('get_event_list/', view_if.get_event_list),
    # # ex: /api/get_guest_list/
    # path('get_guest_list/', view_if.get_guest_list),
    # # ex: /api/user_sign/
    # path('user_sign/', view_if.user_sign),
    #
    # path('get_event_list_sec/', view_if_sec.sec_get_event_list),
]
