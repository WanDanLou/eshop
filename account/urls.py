from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^login_user/$',views.login_user, name = 'login_user'),
    url(r'^register_user/$',views.register_user, name = 'register_user'),
    url(r'^edit_user/$',views.edit_user, name = 'edit_user'),
    url(r'^logout_user$', views.logout_user, name='logout_user'),
    url(r'^change_user_password$', views.change_user_password, name='change_user_password'),
]
