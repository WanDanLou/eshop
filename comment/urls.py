from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^create_comment/$',views.create_comment, name = 'create_comment'),
]
