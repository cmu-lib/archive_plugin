from django import forms

class ArchiveAdminForm(forms.Form):
    archiving_enabled = forms.BooleanField(required=False)