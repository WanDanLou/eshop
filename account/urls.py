from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete

urlpatterns = [
    url(r'^login_user/$',views.login_user, name = 'login_user'),
    url(r'^register_user/$',views.register_user, name = 'register_user'),
    url(r'^edit_user/$',views.edit_user, name = 'edit_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^change_user_password/$', views.change_user_password, name='change_user_password'),
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),
]
