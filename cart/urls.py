from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index_cart/$', views.index_cart, name='index_cart'),
    url(r'^add_cart/(?P<product_id>\d+)/$', views.add_cart, name='add_cart'),
    url(r'^remove_cart/(?P<product_id>\d+)/$', views.remove_cart, name='remove_cart'),
]
