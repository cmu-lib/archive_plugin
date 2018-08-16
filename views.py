from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse

from plugins.archive_plugin import forms, plugin_settings

from utils import setting_handler, models
from utils.notify_helpers import send_email_with_body_from_user
from security.decorators import editor_user_required, author_user_required

from submission.models import Article
from journal.models import Issue
from models import Version

@editor_user_required
def index(request):
    """
    Creates the admin page for turning the plugin's elements on or off
    """
    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)
    
    journal_archive_enabled = setting_handler.get_plugin_setting(plugin, 'journal_archive_enabled', request.journal, create=True,
                                                        pretty='Enable Journal Archive Display', types='boolean').processed_value
    article_archive_enabled = setting_handler.get_plugin_setting(plugin, 'article_archive_enabled', request.journal, create=True,
                                                        pretty='Enable Article Archive Display', types='boolean').processed_value
    edit_article_enabled = setting_handler.get_plugin_setting(plugin, 'edit_archive_enabled', request.journal, create=True,
                                                        pretty='Enable Article Editing and Updating', types='boolean').processed_value
    request_template = setting_handler.get_plugin_setting(plugin, 'request_email_template', request.journal, create=True,
                                                        pretty='Request Email Template', types='rich-text').processed_value
    
    admin_form = forms.ArchiveAdminForm(initial={'journal_archive_enabled': journal_archive_enabled, 
                                                'article_archive_enabled': article_archive_enabled,
                                                'edit_article_enabled': edit_article_enabled,
                                                'request_template': request_template})

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


def journal_archive(request):
    """
    Display list of overall journal archives
    """
    journal_versions = Issue.objects.filter(journal=request.journal).order_by('-date')
    context = {'journal_versions': journal_versions}
    template = "archive_plugin/journal_version_list.html"

    return render(request, template, context)


def article_archive(request, article_id):
    """
    :article_id = an int representing the pk of the article requested
    Displays a list of previous version of an article
    """
    article = get_object_or_404(Article, pk=article_id)
    base_article = Article.objects.get(pk=article.version.base_article.pk)

    # need to deal with possibility update for article has been submitted but not published
    versions = Article.objects.filter(version__base_article=base_article.pk).order_by('-date_published')
    # versions = base_article.version_set.all()

    template = "archive_plugin/article_version_list.html"
    context = {'main_article': base_article, 'versions': versions}

    return render(request, template, context)

@author_user_required
def update_article_prompt(request, article_id):
    """
    Prompts the user to select whether their edit is major or minor
    : article_id is the pk of the article
    """
    article = get_object_or_404(Article, pk=article_id)
    
    template = 'archive_plugin/inject_edit_article_selector.html'
    context = {'article': article}
    
    return render(request, template, context)

@author_user_required
def update_article(request, article_id, base_article_id):
    """
    Registers a new article as an update of the original article
    : article_id is the pk of the article the user is currently submitting
    : base_article is the pk of the original article this is updating
    The relationship between multiple articles is traced via publication dates
    """
    if request.POST: # a gift for Andy
        update_type = request.POST.get('update_type')
        if update_type != 'new':
            article = get_object_or_404(Article, pk=article_id)
            base_article = get_object_or_404(Article, pk=base_article_id)
            update = Version(article=article, base_article=base_article, update_type=update_type)
            update.save()

    # need to establish redirects for this function - where to go once update is registered?

@editor_user_required
def request_update(request, article_id):
    """
    Processes request from editor to have an entry updated, sends email to registered article owner with update request.
    article_id is pk of the article to be updated
    """
    article = get_object_or_404(Article, pk=article_id)
    subject = "{} Article Update Request: '{}'".format(article.journal.code, article.title)
    to = article.owner.email
    owner_name = article.owner.first_name + " " + article.owner.last_name
    body = """
            <p>Dear {0},</p>
            <p>The editorial board of <i>{1}</i> requests that an article for which you are marked as the owner, '{2},' be updated. Please follow the link below to begin the submission process.</p>
            <p>Best,<br>Editorial Board, <i>{1}</i></p>
    """.format(owner_name, article.journal.name, article.title)

    send_email_with_body_from_user(request, subject, to, body)
    messages.add_message(request, messages.SUCCESS, "Email request sent.")

    return redirect(reverse('manage_archive_article', kwargs={'article_id': article.pk}))


# use utils.notify_helpers function send_email_with_body_from_user(request, subject, to, body, log_dict=None) to email user about update request
# article.authors is many to many - article.authors.all() or use article.owner?