"""
Archive APP: utils.
"""

from .models import NewsletterArchiveWIP, NewsletterArchive
from django.conf import settings
import logging 
import hashlib

from apis.phantomjs_api import PhantomJSAPI
from apis.cloudinary_api import CloudinaryAPI

def save_newsletter_screenshot():
    """
    This function will pick up all newsletter from NewsletterArchiveWIP with status ('1', 'new'),
    send the newsletter url to phantomjs and save the screenshot. After that, it update these newsletters
    stauts to 3(Image received from PhantonJS), or 2(Image sent to PhantonJS) if no image saved.
    """
    new_newsletters = NewsletterArchiveWIP.objects.filter(status='1')
    phantomjs_image_path = "/images/phantomjs/"
    phantomjs_api = PhantomJSAPI()
    for newsletter in new_newsletters:
        file_name = hashlib.md5(newsletter.subject + str(newsletter.publish_date)).hexdigest()
        file_path = "%s%s%s.png" %(settings.MEDIA_ROOT, phantomjs_image_path, file_name)

        if phantomjs_api.get_website_screenshot(newsletter.url, file_path):
            newsletter.image_path_from_phantomjs = "%s%s.png" %(phantomjs_image_path, file_name)
            newsletter.status = '3'
            newsletter.save()
            logging.info("Successfully save image to %s" % file_path)
        else:
            newsletter.status = '2'
            newsletter.save()
            logging.warning("Error happened when get screenshot or save image. path:%s"%file_path)

def upload_images_to_cloudinary():
    """
    This function will pick up all newsletter from NewsletterArchiveWIP with 
    status '3':Image received from PhantonJS, upload those images to cloudinary and save image_id and image_url
    which received from cloudinary. then update those newsletters status to 4(Uploaded on Cloudinary)
    """
    newsletters = NewsletterArchiveWIP.objects.filter(status='3')
    cloudinay_api = CloudinaryAPI()

    for newsletter in newsletters:
        image_path = settings.MEDIA_ROOT + newsletter.image_path_from_phantomjs
        resp = cloudinay_api.upload(image_path)

        newsletter.cloudinary_image_id = resp['public_id']
        newsletter.cloudinary_image_url = resp['secure_url']
        newsletter.status = '4'
        newsletter.save()
        logging.info("Successfully update newsletter: %s" %newsletter.subject)  

def mv_reviewed_newsletter():
    """
    This function will pick up all newsletter from NewsletterArchiveWIP with status '5':reviewed by admin/editor
    mv it to NewsletterArchive model.
    """

    newsletters = NewsletterArchiveWIP.objects.filter(status='5')
    for newsletter in newsletters:
        NewsletterArchive.objects.create(
            subject=newsletter.subject,
            sender=newsletter.sender,
            company=newsletter.company,
            added_by=newsletter.added_by,
            cloudinary_image_url=newsletter.cloudinary_image_url,
            cloudinary_image_id=newsletter.cloudinary_image_id,
            status='6'
        )
