from django import forms

class ArchiveAdminForm(forms.Form):
    journal_archive_enabled = forms.BooleanField(required=False,
                                                label='Journal Archiving',
                                                help_text='Turn on or off automatic archiving of articles in this journal, and link to journal archives from browse page.')
    article_archive_enabled = forms.BooleanField(required=False,
                                                label='Article Archiving',
                                                help_text='Turn on or off link when viewing articles to see their version history.')
    edit_article_enabled = forms.BooleanField(required=False,
                                                label='Article Editing',
                                                help_text='Toggle button for authors to update a published article they submitted, and for editors to request that a published article be updated.')
    request_email_template = forms.CharField(required=True, max_length=500,
                                            label='Email template',
                                            help_text='Template for email sent to author when an editor requests an update.',
                                            widget=forms.Textarea)