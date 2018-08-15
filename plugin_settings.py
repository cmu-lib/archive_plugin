PLUGIN_NAME = 'Archiving Plugin'
DESCRIPTION = 'A plugin for managing archives of previous version of articles'
AUTHOR = 'Drew Stimson and Daniel Evans'
VERSION = '0.1'
SHORT_NAME = 'archive_plugin'
MANAGER_URL = 'archive_index'

from utils import models

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

def hook_registry():
    '''
    Run when sites with hooks are loaded to define function to be run
    '''
    return {'journal_archive_list': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_journal_archive'},
            'article_archive_list': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_article_archive'},
            'edit_article': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_edit_article'},
            'request_edit': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_request_edit'}
            }