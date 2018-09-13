
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
    base_article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.SET_NULL, related_name='children')
    update_type = models.CharField(max_length=20, choices=UPDATE_CHOICES)
    new_author = models.BooleanField(default=False)
    revision_date = models.DateTimeField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    # can tell if version is published by accession version's article.stage attribute
