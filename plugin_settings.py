PLUGIN_NAME = 'Archiving Plugin'
DESCRIPTION = 'A plugin for managing archives of previous version of articles'
AUTHOR = 'Drew Stimson and Daniel Evans'
VERSION = '0.1'
SHORT_NAME = 'archive'
MANAGER_URL = 'archive_index'

from utils import models

def install():
    new_plugin, created = models.Plugin.objects.get_or_create(name=SHORT_NAME, version=VERSION, enabled=True)

    if created:
        print('Plugin {0} installed.'.format(PLUGIN_NAME))
    else:
        print('Plugin {0} is already installed.'.format(PLUGIN_NAME))

    models.PluginSetting.objects.get_or_create(name='archive_enabled', plugin=new_plugin, types='boolean',
                                               pretty_name='Enable Archiving', description='Enable Archiving',
                                               is_translatable=False)

def hook_registry():
    '''
    Run when sites with hooks are loaded to define function to be run
    '''
    return {'archive_list': {'module': 'plugins.archive_plugin.hooks', 'function': 'inject_archive'}}