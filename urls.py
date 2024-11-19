from django.urls import re_path
from plugins.archive_plugin import views

urlpatterns = [
    re_path(r'^$', views.index, name='archive_index'),
    re_path(r'^browse_editions/$', views.journal_archive, name='journal_archive'),
    re_path(r'^article/(?P<article_id>\d+)/$', views.article_archive, name='article_archive'),
    re_path(r'^article/(?P<article_id>\d+)/update_type/$', views.update_article_prompt, name='update_type'),
    re_path(r'^article/(?P<article_id>\d+)/update/$', views.update_article, name='update_article'),
    re_path(r'^article/(?P<article_id>\d+)/request_update/$', views.request_update, name='request_update'),
    re_path(r'^browse_entries/$', views.browse_entries, name='browse_entries'),
    re_path(r'^create_archive/$', views.create_archive, name='create_archive'),
]