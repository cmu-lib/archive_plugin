
from django.db import models
from submission.models import Article, STAGE_PUBLISHED
from journal.models import Issue

UPDATE_TYPE_MINOR = "minor"
UPDATE_TYPE_MAJOR = "major"

UPDATE_CHOICES = [
    (UPDATE_TYPE_MINOR, 'Minor'),
    (UPDATE_TYPE_MAJOR, 'Major')
]

UPDATE_INFO = {
    UPDATE_TYPE_MINOR: 'Correction of a typographical error',
    UPDATE_TYPE_MAJOR: 'Substantive content change, including new bibliographic entries'
}


class Version(models.Model):
    article = models.OneToOneField(Article, null=True, on_delete=models.CASCADE)
    parent_article = models.ForeignKey(Article, null=True, on_delete=models.PROTECT, related_name='updates')
    base_article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.PROTECT, related_name='children')
    update_type = models.CharField(max_length=20, choices=UPDATE_CHOICES)

    @property
    def is_published(self):
        """
        Has this version reached the "Published" stage?"
        """
        return self.article.stage == STAGE_PUBLISHED

    @property
    def update_type_info(self):
        """
        Return human-readable description of the update type.
        """
        return UPDATE_INFO[self.update_type]

    @property
    def revision_date(self):
        """
        Convenience function to get the publication date of the Version
        """
        return self.article.publication_date

    @property
    def changed_author(self):
        """
        Has the corresponding author for this version changed from its parent version?
        """
        return self.article.correspondence_author.pk == self.parent_article.coreespondece_author.pk


class Archive(models.Model):
    issue = models.OneToOneField(Issue, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.issue.issue_title
