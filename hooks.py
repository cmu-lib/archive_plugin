from django.shortcuts import render

from plugins.archive_plugin import plugin_settings
from utils import models, setting_handler

def inject_archive(context):
    request = context.get('request')
    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)

    archive_enabled = setting_handler.get_plugin_setting(plugin, 'archive_enabled', request.journal)

    if not archive_enabled.value:
        return ''

    return render(request, 'archive_plugin/inject.html')

def inject_edit_article(context):
    """
    Inject a form to be injected at the beginning of the submission process
    Prompts user to specify whether submission is new or update to existing article
    If update, asks whether major (substantive content updates) or minor (typos)
    """
    request = context.get('request')
    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)

    edit_archive_enabled = setting_handler.get_plugin_setting(plugin, 'edit_article_enabled', request.journal)

    if not edit_archive_enabled.value:
        return ''

    return render(request, 'archive_plugin/inject_edit_article.html')


def inject_article_archive(context):
    """
    Injects a menu for the user to select a previous version of an article
    """ 
    return ''


def inject_journal_archive(context):
    """
    Injects a menu for the user to select a previous archive of the encyclopedia
    """
    return ''