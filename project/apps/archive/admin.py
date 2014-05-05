"""
archive App: admins
"""
from django.contrib import admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from .models import *
from .forms import *

class NewsletterArchiveAdmin(admin.ModelAdmin):
    """
    admin for NewsletterArchive
    """
    readonly_fields = ('status', 'cloudinary_image_url', 
        'cloudinary_image_id',)

    list_display = ['subject', 'get_company', 'status', 'cloudinary_image_url', 
        'cloudinary_image_id', 'added_by']

    def get_company(self, obj):
        return obj.company.company_name
    get_company.short_description = 'company'

    def has_add_permission(self, request):
        return False  

class NewsletterArchiveWIPAdmin(AjaxSelectAdmin):
    """
    admin for NewsletterArchiveWIP
    """
    form = make_ajax_form(NewsletterArchiveWIP, {'company': 'company_lookup'}, NewsletterArchiveWIPForm)
    readonly_fields = ('status', 'show_cloudinary_url', 'header',
        'cloudinary_image_id', 'image_path_from_phantomjs', 'saved_mongo','timestamp')
    list_filter = ('status',)
    list_display = ['subject', 'get_company', 'status', 'image_path_from_phantomjs', 'show_cloudinary_url', 
        'cloudinary_image_id', 'added_by', 'publish_date']
    actions = ["delete_model", "make_reviewed"]

    def get_company(self, obj):
        if obj.company:
            return obj.company.company_name
        else:
            return None
    get_company.short_description = 'company'

    def show_cloudinary_url(self, obj):
        return '<a href="%s" target="_new">%s</a>' % (obj.cloudinary_image_url, obj.cloudinary_image_url)
    show_cloudinary_url.allow_tags = True

    def make_reviewed(modeladmin, request, queryset):
        """
        This function adds an action to NewsletterArchiveWIP admin page, to make 
        multiple newsletter archive reviewed.
        """
        queryset.update(status='5')
    make_reviewed.short_description = "Mark selected newsletters as reviewed"

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        This will initial added_by field to the current logined user.
        """
        formfield = super(NewsletterArchiveWIPAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "added_by" and kwargs['request'].user:
            formfield.initial = kwargs['request'].user.id
        if db_field.name == 'company':
            myfield_choices_cache = getattr(kwargs['request'], 'myfield_choices_cache', None)
            if myfield_choices_cache is not None:
                formfield.choices = myfield_choices_cache
            else:
                kwargs['request'].myfield_choices_cache = formfield.choices
        return formfield

    def get_actions(self, request):
        actions = super(NewsletterArchiveWIPAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(modeladmin, request, queryset):
        for obj in queryset:
            obj.delete()
    delete_model.short_description = "Delete selected models"


class NewsletterTagAdmin(admin.ModelAdmin):
    """
    Admin for NewsletterTag
    """
    list_display = ['name', 'newsletter_name', 'newsletter_date']
    readonly_fields = ('name', 'newsletter', 'newsletter_date')

    def has_add_permission(self, request):
        return False

    def newsletter_name(self, obj):
        return obj.newsletter.subject
    newsletter_name.short_description = 'newsletter'

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
    list_display = ['company_name', 'domain_names', 'subdomain_names', 'industry', 'company_country']
    form = CompanyDetailForm

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        This will initial added_by field to the current logined user.
        """
        formfield = super(CompanyDetailAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "added_by" and kwargs['request'].user:
            formfield.initial = kwargs['request'].user.id
        return formfield

# Register your models here.
admin.site.register(NewsletterArchive, NewsletterArchiveAdmin)
admin.site.register(NewsletterArchiveWIP, NewsletterArchiveWIPAdmin)
admin.site.register(CompanyDetail, CompanyDetailAdmin)
admin.site.register(NewsletterTag, NewsletterTagAdmin)
admin.site.register(CompanyStatstistics)
admin.site.register(CompanySubdomain, CompanySubdomainAdmin)
admin.site.register(Industry)

