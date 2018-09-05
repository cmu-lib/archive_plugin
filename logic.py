from datetime import datetime

from submission.models import Article
from journal.models import Issue

from archive_plugin.models import Version

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
    article.date_declined = None
    article.date_submitted = None
    article.date_updated = None
    
    # Reset step and stage information
    article.current_step = 1
    article.stage = 'Unsubmitted'

    # Save and return copied article
    article.save()
    return article


def register_update_time(**kwargs):
    """
    Once article published, update its entry in version table to reflect publication date
    Receives two kwargs: request and article
    """

    article = kwargs.get('article')

    if hasattr(article, 'version'):
        v = article.version
        v.revision_date = article.date_published
        v.is_published = True
        v.save()


def run_archive(request):
    """
    Function to automatically run an archive containing all published articles
    Will only include the most recent version of articles with multiple versions
    """
    # get date and convert to string in format 'mm/dd/YYYY'
    curr_date = datetime.now()
    pretty_date = curr_date.strftime('%m/%d/%Y')

    # get list of current, published articles
    articles = list(Article.objects.all().sort_by("title"))

    for article in list(articles):
        if article.updates or article.stage != "Published":
            articles.remove(article)

    # set up info for issue
    title = pretty_date
    volume = None # how should I automatically select?
    issue = None # how should I automatically select?
    date = curr_date
    issue_description = "Archive: " + pretty_date
    issue_type = "Issue"

    new_issue = Issue(journal=request.journal, volume=volume, issue=issue, issue_title=title, date=date, issue_type=issue_type, issue_description=issue_description)
    new_issue.save()
    