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
    # perhaps add "is_published" boolean field to track whether the updated version has been published?

    @property
    def base_article(self):
        """
        Follow tree of parent articles down to the original base_article
        """
        # check if parent article is also an update, if so access its parent recursively
        if hasattr(self.parent_article, 'version'):
            return self.parent_article.version.base_article
        # if parent is not an update, return it
        else:
            return self.parent_article
