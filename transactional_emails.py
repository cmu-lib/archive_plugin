from utils.notify_helpers import send_email_with_body_from_user
from utils import setting_handler, models
from plugins.archive_plugin import plugin_settings

def send_update_request_email(request, article):
    """
    Generate and send email to article correspondence author notifying them of editor's update request
    : article is an article object
    """

    plugin = models.Plugin.objects.get(name=plugin_settings.SHORT_NAME)

    subject = "{} Article Update Request: '{}'".format(article.journal.code, article.title)
    to = article.correspondence_author.email
    body = setting_handler.get_plugin_setting(plugin, 'request_email_template', request.journal, create=False,
                                                pretty='Request Email Template', types='rich-text').processed_value

    send_email_with_body_from_user(request, subject, to, body)
