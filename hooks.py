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