# TODO: figure out what model additions we need

# probably need to track article version with the original article_id, keep dates of submission
# seems like we need an entry for each archive of journal as well

from django.db import models
from submission.models import Article

class Version(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    base_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    update_type = models.CharField(max_length=20)
    new_author = models.BooleanField(default=False)
    revision_date = models.DateTimeField(blank=True, null=True)

# will having multiple relationships of different types (one-to-one and many-to-one) to submission.Article work?