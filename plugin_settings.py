PLUGIN_NAME = 'Archiving Plugin'
DESCRIPTION = 'A plugin for managing archives of previous version of articles'
AUTHOR = 'Drew Stimson and Daniel Evans'
VERSION = '0.1'
SHORT_NAME = 'archive_plugin'
MANAGER_URL = 'archive_index'

from utils import models, setting_handler
from journal.models import Journal
from events import logic as event_logic
from plugins.archive_plugin.events import register_update_time


event_logic.Events.register_for_event(event_logic.Events.ON_AUTHOR_PUBLICATION, register_update_time)


def install():
    new_plugin, created = models.Plugin.objects.get_or_create(name=SHORT_NAME, version=VERSION, enabled=True)

    if created:
        print('Plugin {0} installed.'.format(PLUGIN_NAME))
    else:
        print('Plugin {0} is already installed.'.format(PLUGIN_NAME))

    models.PluginSetting.objects.get_or_create(name='journal_archive_enabled', plugin=new_plugin, types='boolean',
                                               pretty_name='Enable Journal Archive Display',
                                               description='Enable Journal Archive Display',
                                               is_translatable=False)
    models.PluginSetting.objects.get_or_create(name='article_archive_enabled', plugin=new_plugin, types='boolean',
                                               pretty_name='Enable Article Archive Display',
                                               description='Enable Article Archive Diesplay',
                                               is_translatable=False)
    models.PluginSetting.objects.get_or_create(name='edit_article_enabled', plugin=new_plugin, types='boolean',
                                               pretty_name='Enable Article Editing and Updating',
                                               description='Enable Article Editing and Updating',
                                               is_translatable=False)
    models.PluginSetting.objects.get_or_create(name='request_email_template', plugin=new_plugin, types='rich-text',
                                               pretty_name='Request Email Template',
                                               description='Template for the email sent to authors '
                                                           'when an editor requests an article be updated',
                                               is_translatable=False)

    message_text = """
        <p>Dear {{ article.correspondence_author.full_name }},</p>
        <p>The editorial board of <i>{{ article.journal.name }}</i> requests that the article, '{{ article.title }},' be updated. Please follow the link below to begin the submission process.</p>
        <p><a href="{{ request.journal_base_url }}{% url 'update_type' article.pk %}">Submit your update.</a></p>
        <p>Best,<br>Editorial Board, <i>{{ article.journal.name }}</i></p>
    """

    # set starting message template for each journal
    for journal in Journal.objects.all():
        setting_handler.save_plugin_setting(new_plugin, 'request_email_template', message_text, journal)
        # TODO: make archive interval a setting


def hook_registry():
    """
    Run when sites with hooks are loaded to define function to be run
    """
    return {'journal_archive_list': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_journal_archive'},
            'article_archive_list': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_article_archive'},
            'article_archive_warning': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_article_archive_warning'},
            'edit_article': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_edit_article'},
            'request_edit': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_request_edit_update'}
            }
