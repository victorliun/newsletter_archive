from django.contrib import admin

from models import *

class NewsletterArchiveWIPAdmin(admin.ModelAdmin):
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


# Register your models here.
admin.site.register(NewsletterArchive)
admin.site.register(NewsletterArchiveWIP, NewsletterArchiveWIPAdmin)
admin.site.register(CompanyDetail)
admin.site.register(NewsletterTag)
admin.site.register(CompanyStatstistics)

