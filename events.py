
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
