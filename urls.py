from django.conf.urls import url
from plugins.archive_plugin import views

url_patterns = [
    url(r'^$', views.index, name='archive_index'),
    url(r'^journal/$', views.journal_archive, name='journal_archive'),
    url(r'^journal/(?P<archive_id>\d+)/$', views.archive_list, name='archive_list'),
    url(r'^article/(?P<article_id>\d+)/$', views.article_archive, name='article_archive'),
    url(r'^article/(?P<article_id>\d+)/update/$', views.update_article, name='update_article'),
    url(r'^view_archive/$', views.view_archive, name='archive_view'),
]

# add separate urls for article and journal archive views