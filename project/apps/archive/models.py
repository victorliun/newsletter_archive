"""
Archive App: models.
"""
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import permalink
from django.utils.text import slugify
from datetime import datetime

import logging
from lxml import etree
from django_countries.fields import CountryField

from apis.cloudinary_api import CloudinaryAPI

class Industry(models.Model):
    """
    Model of Industry, for company.
    """
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.description
    class Meta:
        verbose_name_plural = 'Industries'

class CompanyDetail(models.Model):
    """
    Model of table: CompanyDetail.
    This table keep recording details of eche company.
    Fields include:
        > id: default field
        > company_name: the name of company
        > company_county: which country this company belongs to
        > domain_names: the domain names that company have
        > company_tags: tags this company
        > added_by: who add this entry
        > unsubscribe_url: the url used to unsubscribe it
        > subscribe_url: the url used to subscribe it
        > unsubscribe_email: the email used to unsubscribe it
        > slug: the readable url for each record intead of using record's id
    """
    
    company_name = models.CharField(max_length=20)
    company_country = CountryField()
    industry = models.ForeignKey(Industry, blank=True, null=True)
    domain_names = models.CharField(max_length=255)
    subdomain_names = models.CharField(max_length=255, blank=True)
    company_tags = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name="company_added_by")
    unsubscribe_url = models.URLField(blank=True)
    subscribe_url = models.URLField(blank=True)
    unsubscribe_email = models.EmailField(blank=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        """
        Returns the company id, name and domains.
        """

        return u"Company:%d, %s - %s" %(self.pk, self.company_name, self.domain_names)


    def save(self, *args, **kwargs):
        """
        First this generate a string for slug field if it's null.
        """
        
        if not self.slug:
            self.slug = slugify(unicode(self.company_name))

        super(CompanyDetail, self).save(*args, **kwargs)

        for subdomain in self.subdomains:
            if subdomain and not CompanySubdomain.objects.filter(subdomain__iexact=subdomain).count():
                CompanySubdomain.objects.create(subdomain=subdomain, company=self)
        
    @property
    def domains(self):
        """
        Return a list of domains. domain_names field is a comma seperated string.
        """

        return filter(None, map(lambda x: x.strip(), self.domain_names.split(',')))

    @property
    def subdomains(self):
        """
        Return a list of subdomains. subdomain_names field is a comma seperated string.
        """
        if self.subdomain_names:
            return filter(None, map(lambda x: x.strip(), self.subdomain_names.split(',')))
        else:
            return []

    @property
    def tags(self):
        """
        Return a list of domains. domain_names field is a comma seperated string.
        """

        return filter(None, map(lambda x: x.strip(), self.company_tags.split(',')))

#NEWSLETTER_ARCHIVE_STATUS indicates each status of newsletter archive, different newsletter will 
#be processed by diffirent jobs.
NEWSLETTER_ARCHIVE_STATUS = (
    ('1', 'New'),
    ('2', 'Sent Newletter URL to Phantom JS'),
    ('3', 'Image received from PhantonJS'),
    ('4', 'Uploaded on Cloudinary'),
    ('5', 'Reviewed by Admin/ Editor'),
    ('6', 'Published (moved to the final table)'),
)

class NewsletterArchive(models.Model):
    """
    Model Name: NewsletterArchive, store follow information of a newsletter archive.
        > subject: newsletter subject
        > sender: email address of sender
        > header: newsletter email's head information
        > publish_date: On which date this newsletter archived
        > company: Which company this newsletter come from
        > added_by: Who archived this newsletter
        > cloudinary_image_url: the image url from cloudinary where store newsletter archive images
        > cloudinary_image_id: the image url from cloudinary where store newsletter archive images
        > status: indicates which status this newsletter archive is in. for this table this is all 6.
    """
    subject = models.CharField(max_length=255)
    sender = models.EmailField()
    publish_date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(CompanyDetail, related_name="company")
    added_by = models.ForeignKey(User, related_name="added_by")
    cloudinary_image_url = models.URLField(blank=True)
    cloudinary_image_id = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length='1', choices=NEWSLETTER_ARCHIVE_STATUS, default='6')

    def __unicode__(self):
        """
        Return a string of company and publish_date
        """
        return u"Newsletter from %s, Published on %s" %(self.company, self.publish_date)
 
class NewsletterArchiveWIP(models.Model):
    """
    Model Name: NewsletterArchiveWIP, store follow information of a newsletter archive.
        > subject: newsletter subject
        > publish_date: On which date this newsletter Published
        > sender: email address of sender
        > header: newsletter email's head information
        > company: Which company this newsletter come from
        > added_by: Who archived this newsletter
        > cloudinary_image_url: the image url from cloudinary where store newsletter archive images
        > cloudinary_image_id: the image url from cloudinary where store newsletter archive images
        > status: indicates which status this newsletter archive is in.
        > tags: tag this newsletter
        > url: the original url of newsletter
        > image_path_from_phantomjs: the temprary path where save the image
        > reviewed: if this record reviewed by editor or admin.
        > saved_mongo: indicate whether it saved to mongodb or not.
        > timestamp: when this record added to db
    """
    subject = models.CharField(max_length=255)
    publish_date = models.DateField(default=datetime.now)
    sender = models.EmailField()
    header = models.TextField()
    company = models.ForeignKey(CompanyDetail, related_name="wip_company", null=True, blank=True)
    added_by = models.ForeignKey(User, related_name="wip_added_by")
    cloudinary_image_url = models.URLField(blank=True)
    cloudinary_image_id = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length='1', choices=NEWSLETTER_ARCHIVE_STATUS, default='1')
    newsletter_tags = models.CharField(max_length=255)
    url = models.URLField()
    image_path_from_phantomjs = models.CharField(max_length=80, blank=True)
    reviewed = models.BooleanField(default=False)
    saved_mongo = models.BooleanField(default=False)
    timestamp = models.DateField(default=datetime.now())

    def __unicode__(self):
        """
        Return a string of company and publish_date
        """
        return u"Newsletter from %s, Published on %s" %(self.company, self.publish_date)

    @property
    def tags(self):
        """
        return a list of tags
        """
        return filter(None, map(lambda x: x.strip(), self.newsletter_tags.split(',')))


    def save(self, *args, **kwargs):
        """
        Save new tags to newslettertag table
        """
        super(NewsletterArchiveWIP, self).save(*args, **kwargs)
        # save tags of this newsletter to newsletter tags table
        for tag in self.tags:
            NewsletterTag.objects.get_or_create(newsletter=self, name=tag, newsletter_date=self.publish_date)
        # save tags of company of this newsletter to newsletter tags table
        if self.company is not None:
            for tag in self.company.tags:
                NewsletterTag.objects.get_or_create(newsletter=self, name=tag, newsletter_date=self.publish_date)

    def delete(self, *args, **kwargs):
        """
        delete newsletter_archive WIP, also delete the cloudinary image
        """
        if self.cloudinary_image_id:
            c_api = CloudinaryAPI()
            res = c_api.uploader.destroy(self.cloudinary_image_id)
            logging.info("deleted %s, %s" %(self.cloudinary_image_id, res)) 
        super(NewsletterArchiveWIP, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Newsletter archive-wips'


class NewsletterTag(models.Model):
    """
    Model for newslettertag. thest tags generated from company tags field and 
    newsletter tags fields.
        > Id: auto increase
        > name: tag's name, Must unique
        > newsletter: where is this tag from 
    """
    name = models.CharField(max_length=40, null=False, unique=False)   
    newsletter = models.ForeignKey(NewsletterArchiveWIP, null=True)
    newsletter_date = models.DateField()
    
    def __unicode__(self):
        """
        Return a string as the description of this tag.
        """
        return u"Tag: %s: Newsletter: %s" %(self.name, self.newsletter)

    class Meta:
        unique_together = (("name", "newsletter"),)


class CompanyStatstistics(models.Model):
    """
    Model for CompanyStatstistics: 
    fields:
        > company: associated to CompanyDetail.
        > newsletter_archived: how many Newsletter archived.
        > newsletter_views: how many newsletter viewed.
        > last_update: last_update time.
    """
    company = models.OneToOneField(CompanyDetail, primary_key=True, related_name="companystatstistics")
    newsletter_archived = models.IntegerField(default=0)
    newsletter_views = models.IntegerField(default=0)
    last_update = models.DateField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        """
        return string of company statstistics.
        """
        return u"%s, has %d newsletters archived, %d newsletters viewed, last_update: %s" %(
            self.company, self.newsletter_archived, self.newsletter_views, self.last_update)
    
    class Meta:
        verbose_name_plural = 'Company Statstistics'


class CompanySubdomain(models.Model):
    """
    Models for Company subdomains.
        > company: which company.
        > subdomain: subdomain of the company.
    """

    company = models.ForeignKey(CompanyDetail, related_name="company_subdomain")
    subdomain = models.URLField()

    def __unicode__(self):
        """
        return string of company subdomain.
        """
        return u"%s - %s"%(self.company, self.subdomain)