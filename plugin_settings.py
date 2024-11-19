PLUGIN_NAME = 'Archiving Plugin'
DESCRIPTION = 'A plugin for managing archives of previous version of articles'
AUTHOR = 'Drew Stimson and Daniel Evans'
VERSION = '0.1'
SHORT_NAME = 'archive_plugin'
MANAGER_URL = 'archive_index'

from utils import setting_handler
from utils import plugins
from utils.install import update_settings
from journal.models import Journal

class ArchivePlugin(plugins.Plugin):
    plugin_name = PLUGIN_NAME
    display_name = PLUGIN_NAME
    description = DESCRIPTION
    author = AUTHOR
    short_name = SHORT_NAME
    manager_url = MANAGER_URL
    version = VERSION
    janeway_version = "1.7.0"
    is_workflow_plugin = False

def install():
    ArchivePlugin.install()
    update_settings(
        file_path='plugins/archive_plugin/install/settings.json',
    )

# def install():
#     new_plugin, created = models.Plugin.objects.get_or_create(name=SHORT_NAME, version=VERSION, enabled=True)

#     if created:
#         print('Plugin {0} installed.'.format(PLUGIN_NAME))
#     else:
#         print('Plugin {0} is already installed.'.format(PLUGIN_NAME))

#     models.PluginSetting.objects.get_or_create(name='journal_archive_enabled', plugin=new_plugin, types='boolean',
#                                                pretty_name='Enable Journal Archive Display',
#                                                description='Enable Journal Archive Display',
#                                                is_translatable=False)
#     models.PluginSetting.objects.get_or_create(name='article_archive_enabled', plugin=new_plugin, types='boolean',
#                                                pretty_name='Enable Article Archive Display',
#                                                description='Enable Article Archive Diesplay',
#                                                is_translatable=False)
#     models.PluginSetting.objects.get_or_create(name='edit_article_enabled', plugin=new_plugin, types='boolean',
#                                                pretty_name='Enable Article Editing and Updating',
#                                                description='Enable Article Editing and Updating',
#                                                is_translatable=False)
#     models.PluginSetting.objects.get_or_create(name='request_email_template', plugin=new_plugin, types='rich-text',
#                                                pretty_name='Request Email Template',
#                                                description='Template for the email sent to authors '
#                                                            'when an editor requests an article be updated',
#                                                is_translatable=False)
#     models.PluginSetting.objects.get_or_create(name='archive_search_filter_enabled', plugin=new_plugin, types='boolean',
#                                                pretty_name='Only show new versions of article on search',
#                                                description='Suppress old article versions',
#                                                is_translatable=False)

#     message_text = """
#         <p>Dear {{ article.correspondence_author.full_name }},</p>
#         <p>The editorial board of <i>{{ article.journal.name }}</i> requests that the article, '{{ article.title }},' be updated. Please follow the link below to begin the submission process.</p>
#         <p><a href="{{ request.journal_base_url }}{% url 'update_type' article.pk %}">Submit your update.</a></p>
#         <p>Best,<br>Editorial Board, <i>{{ article.journal.name }}</i></p>
#     """

#     # set starting message template for each journal
#     for journal in Journal.objects.all():
#         setting_handler.save_plugin_setting(new_plugin, 'request_email_template', message_text, journal)
#         # TODO: make archive interval a setting


def hook_registry():
    """
    Run when sites with hooks are loaded to define function to be run
    """
    return {'journal_archive_list': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_journal_archive'},
            'article_archive_list': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_article_archive'},
            'article_archive_warning': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_article_archive_warning'},
            'edit_article': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_edit_article'},
            'request_edit': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_request_edit_update'},
            'filter_search': {'module': 'plugins.archive_plugin.hooks', 'function': 'reconfigure_archive_search'}
            }

