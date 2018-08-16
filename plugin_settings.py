PLUGIN_NAME = 'Archiving Plugin'
DESCRIPTION = 'A plugin for managing archives of previous version of articles'
AUTHOR = 'Drew Stimson and Daniel Evans'
VERSION = '0.1'
SHORT_NAME = 'archive_plugin'
MANAGER_URL = 'archive_index'

from utils import models, setting_handler

def install():
    new_plugin, created = models.Plugin.objects.get_or_create(name=SHORT_NAME, version=VERSION, enabled=True)

    if created:
        print('Plugin {0} installed.'.format(PLUGIN_NAME))
    else:
        print('Plugin {0} is already installed.'.format(PLUGIN_NAME))

    models.PluginSetting.objects.get_or_create(name='journal_archive_enabled', plugin=new_plugin, types='boolean',
                                               pretty_name='Enable Journal Archive Display', description='Enable Journal Archive Display',
                                               is_translatable=False)
    models.PluginSetting.objects.get_or_create(name='article_archive_enabled', plugin=new_plugin, types='boolean',
                                                pretty_name='Enable Article Archive Display', description='Enable Article Archive Diesplay',
                                                is_translatable=False)
    models.PluginSetting.objects.get_or_create(name='edit_article_enabled', plugin=new_plugin, types='boolean',
                                                pretty_name='Enable Article Editing and Updating', description='Enable Article Editing and Updating',
                                                is_translatable=False)
    models.PluginSetting.objects.get_or_create(name='request_email_template', plugin=new_plugin, types='rich-text',
                                                pretty_name='Request Email Template',
                                                description='Template for the email sent to authors when an editor requests an article be updated',
                                                is_translatable=False)

    # Where does I initially set the template for the email message?
    message_text = """
        <p>Dear {{ article.owner.full_name }},</p>
        <p>The editorial board of <i>{{ request.journal.name }}</i> requests that an article for which you are marked as the owner, '{{ article.title }},' be updated. Please follow the link below to begin the submission process.</p>
        <p><a href="{{ request.journal_base_url }}{% url 'inject_edit_article_selector' article.pk %}">Submit your update.</a></p>
        <p>Best,<br>Editorial Board, <i>{{ request.journal.code }}</i></p>
    """
    setting_handler.save_plugin_setting(new_plugin, 'request_email_template', message_text, request.journal)


def hook_registry():
    '''
    Run when sites with hooks are loaded to define function to be run
    '''
    return {'journal_archive_list': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_journal_archive'},
            'article_archive_list': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_article_archive'},
            'edit_article': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_edit_article'},
            'request_edit': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_request_edit'}
            }