from django.template.loader import render_to_string

from plugins.archive_plugin import plugin_settings
from utils import models, setting_handler

from plugins.archive_plugin import views

def inject_edit_article(context):
    """
    Inject a button into dashboard article management page that allows authors to submit an article update
    """
    request = context.get('request')
    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)

    edit_article_enabled = setting_handler.get_plugin_setting(plugin, 'edit_article_enabled', request.journal)

    if not edit_article_enabled.value:
        return ''

    return render_to_string(
        'archive_plugin/inject_edit_article.html',
        context={'article': context.get('article')},
        request=request
    )

def inject_article_archive_warning(context):
    """
    Injects a warning that an article has a more recent published version available.
    """

    request = context.get('request')
    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)

    article_archive_enabled = setting_handler.get_plugin_setting(plugin, 'article_archive_enabled', request.journal)

    if not article_archive_enabled.value:
        return ''

    article = context.get('article')

    # If the article has never been updated, return nothing
    if not article.updates.exists():
        return ''

    return render_to_string(
        'archive_plugin/inject_article_archive_warning.html',
        context={'article': context.get('article')},
        request=request
    )

def inject_article_archive(context):
    """
    Injects a link for the user to browse previous version of an article
    """
    request = context.get('request')
    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)

    article_archive_enabled = setting_handler.get_plugin_setting(plugin, 'article_archive_enabled', request.journal)

    if not article_archive_enabled.value:
        return ''

    return render_to_string(
        'archive_plugin/inject_article_archive.html',
        context={'article': context.get('article')},
        request=request
    )


def inject_journal_archive(context):
    """
    Injects a link for the user to browse a list of previous archives of the encyclopedia
    """
    request = context.get('request')
    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)

    journal_archive_enabled = setting_handler.get_plugin_setting(plugin, 'journal_archive_enabled', request.journal)

    if not journal_archive_enabled.value:
        return ''

    return render_to_string('archive_plugin/inject_journal_archive.html', request=request)


def inject_request_edit_update(context):
    """
    Injects a button for editors to request that an article be edited
    """
    request = context.get('request')
    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)

    edit_article_enabled = setting_handler.get_plugin_setting(plugin, 'edit_article_enabled', request.journal)

    if not edit_article_enabled.value:
        return ''

    return render_to_string(
        'archive_plugin/inject_request_edit_update.html',
        context={'article': context.get('article')},
        request=request
    )

def reconfigure_archive_search(context):
    """
    captures incoming article_list from search and adds filter to query string to show only latest versions of articles.
    """
    request = context.get('request')
    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)

    archive_search_filter_enabled = setting_handler.get_plugin_setting(plugin, 'archive_search_filter_enabled', request.journal)
    if archive_search_filter_enabled.value:
        articles_qs = context.get('articles')
        excluded_articles_qs = views.archive_filter_search(articles_qs)
        context['articles'] = excluded_articles_qs
    return ""
