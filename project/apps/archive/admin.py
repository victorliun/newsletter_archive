from django.contrib import admin

from .models import *
from .forms import *

class NewsletterArchiveWIPAdmin(admin.ModelAdmin):
    """
    admin for NewsletterArchiveWIP
    """
    form = NewsletterArchiveWIPForm
    readonly_fields = ('status', 'cloudinary_image_url', 'header',
        'clouninary_image_id', 'image_path_from_phantomjs')
    list_filter = ('status',)
    list_display = ['company', 'status', 'cloudinary_image_url', 
        'clouninary_image_id', 'added_by']
    actions = ["make_reviewed"]

    def make_reviewed(modeladmin, request, queryset):
        """
        This function adds an action to NewsletterArchiveWIP admin page, to make 
        multiple newsletter archive reviewed.
        """
        queryset.update(status='5')
    make_reviewed.short_description = "Mark selected newsletters as reviewed"

class NewsletterTagAdmin(admin.ModelAdmin):
    """
    Admin for NewsletterTag
    """
    list_display = ['name', 'newsletter', 'from_company']
    readonly_fields = ('name', 'newsletter', 'from_company')

    def has_add_permission(self, request):
        return False

class CompanySubdomainAdmin(admin.ModelAdmin):
    """
    Admin for CompanySubdomain
    """
    list_display = ['company', 'subdomain',]
    def has_add_permission(self, request):
        return False  

class CompanyDetailAdmin(admin.ModelAdmin):
    """
    Admin for CompanyDetail
    """
    list_display = ['company_name', 'subdomain_names',  'company_country']
    form = CompanyDetailForm


# Register your models here.
admin.site.register(NewsletterArchive)
admin.site.register(NewsletterArchiveWIP, NewsletterArchiveWIPAdmin)
admin.site.register(CompanyDetail, CompanyDetailAdmin)
admin.site.register(NewsletterTag, NewsletterTagAdmin)
admin.site.register(CompanyStatstistics)
admin.site.register(CompanySubdomain, CompanySubdomainAdmin)

