# TODO: figure out what model additions we need

# probably need to track article version with the original article_id, keep dates of submission
# seems like we need an entry for each archive of journal as well

from django.db import models
from submission.models import Article

UPDATE_TYPES = (('m', 'Minor'), ('M', 'Major'))

class ArticleUpdate(models.Model):
    article_id = models.OneToOneField(Article, on_delete=models.CASCADE, primary_key=True)
    orig_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    update_type = models.CharField(max_length=20, choices=UPDATE_TYPES)
    new_author = models.BooleanField()
    revision_date = models.DateTimeField(blank=True, null=True)