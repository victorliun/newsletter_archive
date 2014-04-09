from django import forms

from .models import CompanyDetail, NewsletterArchiveWIP


class CompanyDetailForm(forms.ModelForm):
    """
    Form for CompanyDetail models
    """

    class Meta:
        model = CompanyDetail
        widgets = {
            'domain_names': forms.TextInput(attrs={
                'placeholder': 'Multiple domains must be separated by comma',
                'style': "width:300px;"}),
            'company_tags': forms.TextInput(attrs={
                'placeholder': 'Multiple tags must be separated by comma',
                'style': "width:300px;",}),
            'subdomain_names': forms.TextInput(attrs={
                'placeholder': 'Multiple subdomains must be separated by comma',
                'style': "width:300px;",}),
        }

class NewsletterArchiveWIPForm(forms.ModelForm):
    """
    Form for NewsletterArchiveWIP models
    """

    class Meta:
        model = NewsletterArchiveWIP
        widgets = {
            'newsletter_tags': forms.TextInput(attrs={
                'placeholder': 'Multiple tags must be separated by comma',
                'style': "width:300px;",}),
        }