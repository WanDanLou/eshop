from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^create_order/$', views.create_order, name='create_order'),
    url(r'^pay_order/(?P<order_id>\d+)/$', views.pay_order, name='pay_order'),
    url(r'^detail_order/(?P<order_id>\d+)/$', views.detail_order, name='detail_order'),
    url(r'^pay_order_done/(?P<order_id>\d+)/$', views.pay_order_done, name='pay_order_done'),
    url(r'^delete_order/(?P<order_id>\d+)/$', views.delete_order, name='delete_order'),
    url(r'^delete_order_done/(?P<order_id>\d+)/$', views.delete_order_done, name='delete_order_done'),
    url(r'^deliver_item/(?P<orderItem_id>\d+)/$', views.deliver_item, name='deliver_item'),
    url(r'^deliver_item_done/(?P<orderItem_id>\d+)/$', views.deliver_item_done, name='deliver_item_done'),
    url(r'^return_item/(?P<orderItem_id>\d+)/$', views.return_item, name='return_item'),
    url(r'^return_item_done/(?P<orderItem_id>\d+)/$', views.return_item_done, name='return_item_done'),
    url(r'^recieve_item/(?P<orderItem_id>\d+)/$', views.recieve_item, name='recieve_item'),
    url(r'^detail_item/(?P<orderItem_id>\d+)/$', views.detail_item, name='detail_item'),
    url(r'^index_orderItem/(?P<store_slug>[-\w]+)/$', views.index_orderItem, name='index_orderItem'),
    url(r'^index_order/$', views.index_order, name='index_order'),
    url(r'^comment_item/(?P<orderItem_id>\d+)/$', views.make_comment, name='comment_item'),
    url(r'^revision_comment/(?P<orderItem_id>\d+)/$', views.revision_comment, name='revision_comment'),
    url(r'^reply_item/(?P<orderItem_id>\d+)/$', views.reply_item, name='reply_item'),
    url(r'^revision_reply/(?P<orderItem_id>\d+)/$', views.revision_reply, name='revision_reply'),
]
