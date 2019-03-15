from django.conf.urls import url
from plugins.archive_plugin import views

urlpatterns = [
    url(r'^$', views.index, name='archive_index'),
    url(r'^journal/$', views.journal_archive, name='journal_archive'),
    url(r'^article/(?P<article_id>\d+)/$', views.article_archive, name='article_archive'),
    url(r'^article/(?P<article_id>\d+)/update_type/$', views.update_article_prompt, name='update_type'),
    url(r'^article/(?P<article_id>\d+)/update/$', views.update_article, name='update_article'),
    url(r'^article/(?P<article_id>\d+)/request_update/$', views.request_update, name='request_update'),
    url(r'^browse_entries/$', views.browse_entries, name='browse_entries'),
    url(r'^search/$', views.search, name='archive_search'),
]