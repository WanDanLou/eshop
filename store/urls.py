from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^login_store/$',views.login_store, name = 'login_store'),
    url(r'^register_store/$',views.register_store, name = 'register_store'),
    url(r'^edit_store/$',views.edit_store, name = 'edit_store'),
    url(r'^logout_store$', views.logout_store, name='logout_store'),
    url(r'^change_password_store$', views.change_password_store, name='change_password_store'),
]
