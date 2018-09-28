# Archiving Plugin

This is a feature plugin for the [Janeway journal management system](https://github.com/BirkbeckCTP/janeway). It adds the ability to create and manage archived versions of a journal (and its articles) which users can then browse.

*N.B. This plugin relies on features that are only present in the most recent master of Janeway. Please update if you haven't.*

## Installation

The steps to install this plugin are as follows:

1. Navigate to your base janeway directory, and go to src/plugins
2. Clone this repository to that directory
3. Navigate back to src, and (with your virtual environment enabled) run `python3 manage.py install_plugins`
4. Make the migrations for the plugin: `python3 manage.py makemigrations archive_plugin`
5. Run migrations: `python3 manage.py migrate`
6. Set up automatic journal archiving if desired: `python3 manage.py run_archive`
7. Restart apache
8. Open your instance of janeway, and for all journals for which you wish to use this plugin, go to manager->plugins, select this plugin, and toggle features.
9. (Optional) To add the plugin's browse functionality for a journal (lists all articles in their most up-to-date, published version), go to manager->content manager, click modify nav, and add a page named Browse with the url `plugins/archive_plugin/browse_entries`, or, if you are using path instead of domain, `journal_code/plugins/archive_plugin/browse_entries`, where 'journal_code' is the code you gave to the journal.

## Manually running an archive
If you want to manually run an archive, ssh into your server, navigate to your janeway install src directory, activate your virtual environment, and run `python3 manage.py create_archive`.
