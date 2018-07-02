from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse

from plugins.disqus import forms
from plugins.disqus import plugin_settings

from utils import setting_handler
from utils import models


def index(request):
    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)
    
    archive_enabled = setting_handler.get_plugin_setting(plugin, 'archive_enabled', request.journal, create=True,
                                                        pretty='Enable Archiving', types='boolean').processed_value
    admin_form = forms.ArchiveAdminForm(initial={'archive_enabled': archive_enabled})

    if request.POST:
        admin_form = forms.ArchiveAdminForm(request.POST)

        if admin_form.is_valid():
            for setting_name, setting_value in admin_form.cleaned_data.items():
                setting_handler.save_plugin_setting(plugin, setting_name, setting_value, request.journal)
                messages.add_message(request, messages.SUCCESS, '{0} setting updated.'.format(setting_name))

            return redirect(reverse('archive_index'))

    template = "archive_plugin/index.html"
    context = {
        'admin_form': admin_form,
    }

    return render(request, template, context)


def view_archive(request):
    pass
    # TODO: write logic for querying database, viewing the relevant archived version of journal or article
    # may need to write two versions of function based on whether viewing archived version of article or journal