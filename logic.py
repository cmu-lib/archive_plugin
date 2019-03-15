from datetime import datetime
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

from submission.models import Article

from plugins.archive_plugin.models import Version


def copy_article_for_update(article_id):
    """
    Create copy of article with passed id,
    Reset applicable fields so it is recognized as new, unaccepted article for review.
    Return copy of article
    """
    
    # Make an exact copy of article
    article = Article.objects.get(pk=article_id)
    article.pk = None
    article.save()

    # Reset date information
    article.date_started = datetime.now()
    article.date_accepted = None
    article.date_published = None
    article.date_declined = None
    article.date_submitted = None
    article.date_updated = None
    
    # Reset step and stage information
    article.current_step = 1
    article.stage = "Unsubmitted"

    # Save and return copied article
    article.save()
    return article


def get_base_article(article_id=None):
    """
    Takes an article and gets its base article - for use with registering a new version
    """
    article = get_object_or_404(Article, pk=article_id)

    if hasattr(article, 'version'):
        return get_base_article(article.version.parent_article.pk)
    else:
        return article

def handle_search_controls(request):
    if request.POST:
        
        # being set by get-- still need to grab these in case of post for filtering option.
        search_term = request.POST.get('article_search', False)
        keyword = request.POST.get('keyword', False)

        if not keyword and not search_term:    
            search_term = request.GET.get('article_search', False)
            keyword = request.GET.get('keyword', False)

        sort = request.POST.get('sort', '-date_published')
        if sort:
            search_filters=True
            
        return search_term, keyword, sort, search_filters, set_search_session_variables(request, search_term, keyword, sort, search_filters)

    else:
        search_term = request.GET.get('article_search', False)
        keyword = request.GET.get('keyword', False)
        sort = request.session.get('search_sort','-date_published')
        search_filters = request.session.get('search_filters', False)
                
        return search_term, keyword, sort, search_filters, None

def set_search_session_variables(request, search_term, keyword, sort, search_filters):
    if search_term:
        redir_str = '{0}?article_search={1}'.format(reverse('archive_search'), search_term)
    elif keyword:
        redir_str = '{0}?keyword={1}'.format(reverse('archive_search'), keyword)

    request.session['search_sort'] = sort
    request.session['search_filters'] = search_filters

    return redirect(redir_str)

def unset_search_session_variables(request):
    del request.session['search_sort']
    del request.session['search_filters']

    return redirect('{0}'.format(reverse('archive_search')))

def is_latest(article_list):
    final_articles = []
    for article in article_list:
        is_latest = True
        if hasattr(article, "updates"):
            for update in article.updates.all():
                if update.article.stage == "Published":
                    is_latest = False
        if is_latest:
            final_articles.append(article)
    return final_articles