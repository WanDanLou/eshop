from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^login_user/$',views.login_user, name = 'login_user'),
    url(r'^register_user/$',views.register_user, name = 'register_user'),
    url(r'^edit_user/$',views.edit_user, name = 'edit_user'),
    url(r'^logout_user$', views.logout_user, name='logout_user'),
    url(r'^change_user_password$', views.change_user_password, name='change_user_password'),
    url(r'^product_list$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    url(r'^product_create$', views.product_create, name='product_create'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
