from django import forms

class ArchiveAdminForm(forms.Form):
    journal_archive_enabled = forms.BooleanField(required=False)
    article_archive_enabled = forms.BooleanField(required=False)
    edit_article_enabled = forms.BooleanField(required=False)
    request_email_template = forms.CharField(required=True, max_length=500,
        widget=forms.Textarea)