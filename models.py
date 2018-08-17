# TODO: figure out what model additions we need

# probably need to track article version with the original article_id, keep dates of submission
# seems like we need an entry for each archive of journal as well

from django.db import models
from submission.models import Article

UPDATE_TYPE_MINOR = "minor"
UPDATE_TYPE_MAJOR = "major"

UPDATE_CHOICES = [
    (UPDATE_TYPE_MINOR, 'Minor'),
    (UPDATE_TYPE_MAJOR, 'Major')
]

class Version(models.Model):
    article = models.OneToOneField(Article, null=True, on_delete=models.SET_NULL)
    parent_article = models.ForeignKey(Article, null=True, on_delete=models.SET_NULL, related_name='updates')
    update_type = models.CharField(max_length=20, choices=UPDATE_CHOICES)
    new_author = models.BooleanField(default=False)
    revision_date = models.DateTimeField(blank=True, null=True)

    @property
    def base_article(self):
        """
        Follow parent articles all the way down to the original base_article
        """
        pass

# will having multiple relationships of different types (one-to-one and many-to-one) to submission.Article work?