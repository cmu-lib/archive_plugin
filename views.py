from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from plugins.archive_plugin import forms, plugin_settings, logic, transactional_emails
from plugins.archive_plugin.models import Version

from utils import setting_handler, models
from utils.notify_helpers import send_email_with_body_from_user
from security.decorators import editor_user_required, author_user_required

from submission.models import Article
from journal.models import Issue

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
                                                'request_email_template': request_template})

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
    # can I just do this with the 'journal_issues' url?
    journal_versions = Issue.objects.filter(journal=request.journal).order_by('-date')
    context = {'journal_versions': journal_versions}
    template = "archive_plugin/journal_version_list.html"

    return render(request, template, context)


def article_archive(request, article_id):
    """
    : article_id = an int representing the pk of the article requested
    Displays a list of previous version of an article
    """
    # get current article
    article = get_object_or_404(Article, pk=article_id)

    # ensure current article is either an update or the parent of another article
    if hasattr(article, 'version') or hasattr(article, 'updates'):
        if hasattr(article, 'version'):
            base_article = article.version.base_article
        else:
            base_article = article

        # get queryset of all articles with same base_article (including original base article)
        versions = Article.objects.filter(Q(version__base_article=base_article) | Q(pk=base_article.pk)).filter(stage='Published').order_by('-date_published')

        # prepare and return page
        
        context = {'base_article': base_article, 'versions': versions}

    # if no updates, just return the single entry
    else:
        context = {'base_article': article, 'versions': [article]}

    template = "archive_plugin/article_version_list.html"
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
def update_article(request, article_id):
    """
    Registers a new article as an update of the original article
    : article_id is the pk of the article the user is currently submitting
    : base_article is the pk of the original article this is updating
    The relationship between multiple articles is traced via publication dates
    """
    if request.POST: # a gift for Andy
        update_type = request.POST.get('update_type')
        parent_article = get_object_or_404(Article, pk=article_id)
        new_article = logic.copy_article_for_update(parent_article.pk)
        base_article = logic.get_base_article(parent_article.pk)

        new_version = Version(article=new_article, parent_article=parent_article, update_type=update_type, base_article=base_article)
        new_version.save()

        return redirect(reverse('submit_info', kwargs={'article_id': new_article.pk}))


@editor_user_required
def request_update(request, article_id):
    """
    Processes request from editor to have an entry updated, sends email to registered article owner with update request.
    article_id is pk of the article to be updated
    """
    
    article = get_object_or_404(Article, pk=article_id)
    transactional_emails.send_update_request_email(request, article)

    messages.add_message(request, messages.SUCCESS, "Email request sent.")

    return redirect(reverse('manage_archive_article', kwargs={'article_id': article.pk}))


def browse_entries(request):
    """
    Custom view for browsing all current entries in the encyclopedia
    """
    # get all articles from journal that are published and the most recent copies
    final_articles =  Article.objects.filter(journal=request.journal, stage="Published", updates__isnull=True).order_by("title")

    # set up context and render response
    context = {"articles": final_articles}
    template = "archive_plugin/browse.html"

    return render(request, template, context)