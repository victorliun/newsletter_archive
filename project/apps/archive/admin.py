"""
archive App: admins
"""
from django.contrib import admin

from .models import *
from .forms import *

class NewsletterArchiveAdmin(admin.ModelAdmin):
    """
    admin for NewsletterArchive
    """
    readonly_fields = ('status', 'cloudinary_image_url', 'header',
        'cloudinary_image_id',)

    list_display = ['subject', 'get_company', 'status', 'cloudinary_image_url', 
        'cloudinary_image_id', 'added_by']

    def get_company(self, obj):
        return obj.company.company_name
    get_company.short_description = 'company'

    def has_add_permission(self, request):
        return False  

class NewsletterArchiveWIPAdmin(admin.ModelAdmin):
    """
    admin for NewsletterArchiveWIP
    """
    form = NewsletterArchiveWIPForm
    readonly_fields = ('status', 'cloudinary_image_url', 'header',
        'cloudinary_image_id', 'image_path_from_phantomjs')
    list_filter = ('status',)
    list_display = ['subject', 'get_company', 'status', 'image_path_from_phantomjs', 'cloudinary_image_url', 
        'cloudinary_image_id', 'added_by']
    actions = ["make_reviewed"]

    def get_company(self, obj):
        return obj.company.company_name
    get_company.short_description = 'company'

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
    list_display = ['get_company', 'subdomain',]
    
    def get_company(self, obj):
        return obj.company.company_name
    get_company.short_description = 'company'

    def has_add_permission(self, request):
        return False  

class CompanyDetailAdmin(admin.ModelAdmin):
    """
    Admin for CompanyDetail
    """
    list_display = ['company_name', 'domain_names', 'subdomain_names',  'company_country']
    form = CompanyDetailForm


# Register your models here.
admin.site.register(NewsletterArchive, NewsletterArchiveAdmin)
admin.site.register(NewsletterArchiveWIP, NewsletterArchiveWIPAdmin)
admin.site.register(CompanyDetail, CompanyDetailAdmin)
admin.site.register(NewsletterTag, NewsletterTagAdmin)
admin.site.register(CompanyStatstistics)
admin.site.register(CompanySubdomain, CompanySubdomainAdmin)

