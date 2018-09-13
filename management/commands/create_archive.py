from django.core.management.base import BaseCommand, CommandError

from datetime import datetime

from submission.models import Article
from journal.models import Issue, Journal
from utils import setting_handler, models

from archive_plugin import plugin_settings
from archive_plugin.models import Version

class Command(BaseCommand):
    help = "Run archive issue archive."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        Function to automatically run an archive containing all published articles
        Will only include the most recent version of articles with multiple versions
        """
        plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)
        
        # get date and convert to string in format 'mm/dd/YYYY'
        curr_date = datetime.now()
        pretty_date = curr_date.strftime('%m/%d/%Y')

        # go through each journal and run archive if it is enabled
        for journal in Journal.objects.all():
            # check if journal has archiving enabled
            journal_archive_enabled = setting_handler.get_plugin_setting(plugin, "journal_archive_enabled", journal)

            if journal_archive_enabled.processed_value:

                # set up info for issue
                title = pretty_date
                (volume, issue) = Issue.auto_increment_volume_issue(journal)
                date = curr_date
                issue_description = "Archive run " + pretty_date
                issue_type = "Issue"

                # save initial copy of issue with no articles
                new_issue = Issue(journal=journal, volume=volume, issue=issue, issue_title=title, date=date, issue_type=issue_type, issue_description=issue_description)
                new_issue.save()

                # go through articles for journal, add to issue all that are up-to-date and published
                for article in Article.objects.filter(journal=journal).order_by("title"):
                    if (not hasattr(article, "updates")) and (article.stage == "Published"):
                        new_issue.articles.add(article)
                        if hasattr(article, "version"):
                            v = article.version
                            v.is_archived = True
                            v.save()

                new_issue.save()
