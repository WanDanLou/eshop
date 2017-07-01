from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^login/$',views.authenticate, name = 'login'),
    url(r'^register/$',views.register, name = 'register'),
    url(r'^user_edit/$',views.user_edit, name = 'user_edit'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^change_password$', views.change_password, name='change_password'),
]
