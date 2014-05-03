"""
Archive app: forms
"""
import re

from django import forms

from .models import CompanyDetail, NewsletterArchiveWIP
from django.core.exceptions import ValidationError


class CompanyDetailForm(forms.ModelForm):
    """
    Form for CompanyDetail models
    """

    def clean(self):
        """
        Clean company_tags, subdomain_names and domain_namesfields
        """
        pattern = """
            ^                   # beginning of string
            (                   # start of group #1
               [A-Za-z0-9-]+    # start with the string, at least one letter or number or -
               \.[A-Za-z]{2,}   # continued with . followed by at least two letters
               (                # start group #2
                \.[A-Za-z]{2,}  # continued with . followed by at least two letters.
               )?               # end of group#2, it is optional. 
               [,]?             # followed by comma or not
            )+                  # end of group #1, at least one
            $                   # the end of the string
            """
        pa = re.compile(pattern, re.VERBOSE)
        if not re.search(pa, self.cleaned_data.get('domain_names', '')):
            raise forms.ValidationError("Multiple domains must be separated by comma, invalid domains,%s"\
                %self.cleaned_data.get('domain_names',''))
        if self.cleaned_data.get('subdomain_names', '') and \
            not re.search(pa, self.cleaned_data.get('subdomain_names', '')):
            raise forms.ValidationError("Multiple subdomains must be separated by comma, invalid subdomains")

        tag_pa = re.compile(r"^([A-Za-z0-9\s-]+[,]?)+$")
        if not re.search(tag_pa, self.cleaned_data.get('company_tags','')):
            raise forms.ValidationError("Multiple tag must be separated by comma, invalid tags")
        return self.cleaned_data

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

    def clean_newsletter_tags(self):
        """
        clean newsletter_tags field.
        """
        tag_pa = re.compile(r"^([A-Za-z0-9\s-]+[,]?)+$")
        if not re.search(tag_pa, self.cleaned_data.get('newsletter_tags','')):
            raise ValidationError("Multiple tag must be separated by comma, invalid tags")
        return self.cleaned_data.get('newsletter_tags','')

    class Meta:
        model = NewsletterArchiveWIP
        widgets = {
            'newsletter_tags': forms.TextInput(attrs={
                'placeholder': 'Multiple tags must be separated by comma',
                'style': "width:300px;",}),
            'cloudinary_image_url':forms.TextInput(attrs={'disabled':'disabled'})
        }