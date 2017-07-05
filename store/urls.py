from django.conf.urls import url, include
from . import store_views, product_views
urlpatterns = [
    url(r'^login_store/$',store_views.login_store, name = 'login_store'),
    url(r'^register_store/$',store_views.register_store, name = 'register_store'),
    url(r'^edit_store/$',store_views.edit_store, name = 'edit_store'),
    url(r'^logout_store/$', store_views.logout_store, name='logout_store'),
    url(r'^list_store/$', store_views.list_store, name='list_store'),
    url(r'^change_store_password/$', store_views.change_store_password, name='change_store_password'),
    url(r'^index_store/(?P<store_slug>[-\w]+)/$', store_views.index_store, name='index_store'),
    url(r'^add_product/(?P<store_slug>[-\w]+)/$', product_views.add_product, name='add_product'),
    url(r'^delete_product/(?P<store_slug>[-\w]+)/(?P<product_id>\d+)/$', product_views.delete_product, name='delete_product'),
    url(r'^edit_product/(?P<store_slug>[-\w]+)/(?P<product_id>\d+)/$', product_views.edit_product, name='edit_product'),
    url(r'^list_product/(?P<store_slug>[-\w]+)/$',product_views.list_product, name='list_product'),
    url(r'^detail_product/(?P<store_slug>[-\w]+)/(?P<product_id>\d+)/$', product_views.detail_product, name='detail_product'),
]
