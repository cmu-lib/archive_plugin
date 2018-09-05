from datetime import datetime

from submission.models import Article
from journal.models import Issue, Journal
from utils import setting_handler, models

from archive_plugin import plugin_settings
from archive_plugin.models import Version

def main():
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

        if journal_archive_enabled.value:
            # get list of all articles for journal
            articles = list(Article.objects.filter(journal=journal).sort_by("title"))

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

            new_issue = Issue(journal=journal, volume=volume, issue=issue, issue_title=title, date=date, issue_type=issue_type, issue_description=issue_description)
            new_issue.save()

if __name__ == "__main__":
    main()