from django.conf.urls import url
from plugins.archive_plugin import views

url_patterns = [
    url(r'^$', views.index, name='archive_index'),
    url(r'^view_archive/$', views.view_archive, name='archive_view'),
]