from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^create_order/$', views.create_order, name='create_order'),
    url(r'^pay_order/(?P<order_id>\d+)/$', views.pay_order, name='pay_order'),
    url(r'^detail_order/(?P<order_id>\d+)/$', views.detail_order, name='detail_order'),
    url(r'^pay_order_done/(?P<order_id>\d+)/$', views.pay_order_done, name='pay_order_done'),
    url(r'^delete_order/(?P<order_id>\d+)/$', views.delete_order, name='delete_order'),
    url(r'^delete_order_done/(?P<order_id>\d+)/$', views.delete_order_done, name='delete_order_done'),
    url(r'^index_order/$', views.index_order, name='index_order'),
]
