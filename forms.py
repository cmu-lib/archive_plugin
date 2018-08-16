from django import forms

class ArchiveAdminForm(forms.Form):
    journal_archiving_enabled = forms.BooleanField(required=False)
    article_archivig_enabled = forms.BooleanField(required=False)
    edit_article_enabled = forms.BooleanField(required=False)
    request_template = forms.CharField(required=True, max_length=200,
        widget=forms.Textarea)