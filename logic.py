from datetime import datetime
import copy
from django.shortcuts import get_object_or_404

from submission.models import Article, ArticleAuthorOrder

from plugins.archive_plugin.models import Version


def copy_article_for_update(article_id):
    """
    Create copy of article with passed id,
    Reset applicable fields so it is recognized as new, unaccepted article for review.
    Return copy of article
    """

    # Make an exact copy of article, preserving the original article instance
    # for further queries
    original_article = Article.objects.get(pk=article_id)
    article = copy.copy(original_article)
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

    # Assign all original authors
    original_authors = original_article.authors.all()
    for a in original_authors:
        article.authors.add(a)

    # Assign all original author orders
    original_author_orders = original_article.articleauthororder_set.all()
    for ao in original_author_orders:
        ArticleAuthorOrder.objects.create(article = article, author = ao.author, order = ao.order)

    # Assign all original keywords
    original_keywords = original_article.keywords.all()
    for k in original_keywords:
        article.keywords.add(k)

    # Null out article images so that it is possible to upload new ones
    article.large_image_file = None
    article.thumbnail_image_file = None
    article.meta_image = None

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