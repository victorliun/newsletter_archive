"""
Archive APP: utils.
"""
from django.conf import settings
import logging 
import Queue
import threading
import hashlib
import time
from apps.archive.models import NewsletterArchiveWIP, CompanyDetail, NewsletterArchive
from django.contrib.auth.models import User

from subprocess import Popen
from apis.mail_api import ZMailAPI
from apis.phantomjs_api import PhantomJSAPI
from apis.cloudinary_api import CloudinaryAPI
from pymongo import MongoClient
from os import listdir
import gridfs



def save_newsletter_screenshot():
    """
    This function will pick up all newsletter from NewsletterArchiveWIP with status ('1', 'new'),
    send the newsletter url to phantomjs and save the screenshot. After that, it update these newsletters
    stauts to 3(Image received from PhantonJS), or 2(Image sent to PhantonJS) if no image saved.
    """
    print "Get newsletter webpage screenshot"
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
    print "upload newsletter images to cloudinary"
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
    print "start publish newsletters"
    newsletters = NewsletterArchiveWIP.objects.filter(status='5')
    for newsletter in newsletters:
        NewsletterArchive.objects.get_or_create(
            subject=newsletter.subject,
            sender=newsletter.sender,
            company=newsletter.company,
            added_by=newsletter.added_by,
            cloudinary_image_url=newsletter.cloudinary_image_url,
            cloudinary_image_id=newsletter.cloudinary_image_id,
            status='6',
        )
    newsletters.update(status='6')

def get_newsletters(gmail_account=settings.GMAIL_ACCOUNT, password=settings.GMAIL_PSD, initial=False):
    """
    this function will pick newsletters from an email box. Account sets to defualt gmail account in settings
        > 
    """
    print "search newsletter in inbox"
    automator = User.objects.get_or_create(username='automator')[0]
    api = ZMailAPI(gmail_account, password)
    api.select()
    if initial:
        reps, data = api.search("(ALL)")
    else:
        resp, data = api.search("(UNSEEN)")
    
    mail_ids = data[0].split() #extract email id from response
    for mail_id in mail_ids:
        newsletter_info =  api.process_email(mail_id)
        if newsletter_info:
            newsletter, status = NewsletterArchiveWIP.objects.get_or_create(
                subject=newsletter_info['subject'],
                sender=newsletter_info['sender'][1],
                header=newsletter_info['header'],
                url=newsletter_info['url'],
                publish_date=newsletter_info['publish_date'],
                added_by=automator,
                )

            # search company if exists in our table.
            company_domain = newsletter_info['sender'][1].split('@')[1]
            company = CompanyDetail.objects.filter(domain_names__icontains=company_domain)
            if company.count() == 1:
                newsletter.company = company[0]
                newsletter.save()
            print "store:%s" %newsletter


def save_newsletter_offline(newsletter_url):
    """
    This will save newsletter offline as a package including images, css, js.
    It saves the whole package to the folder
    """

    folder_name = hashlib.md5(newsletter_url).hexdigest()
    folder_path = settings.MEDIA_ROOT + "/newsletter_downloads/" + folder_name
    file_name = newsletter_url.rsplit('/', 1)[0]
    command = "wget"
    args = " -E -H -k -K -p -nd -P %s -e robots=off -o logwget.txt %s" %(folder_path, newsletter_url)
    args = args.split(';')[0] # cut off string after ; if any.
    #subp = check_call(command + args, shell=True)
    proc = Popen(command + args, shell=True)
    proc.communicate() # wait until finish
    return folder_path, file_name


def save_offline_newsletter_to_mongodb():
    """
    This function will save offline newsletter html including images css and js file to 
    mongodb
    """
    print "Start save newsletter offline and save it to  mongodb"
    db = MongoClient().newsletter
    archive = db.archive
    fs = gridfs.GridFS(db, 'archive')

    newsletters = NewsletterArchiveWIP.objects.filter(status='6', saved_mongo=False)

    for newsletter in newsletters:
        folder_path, index_name = save_newsletter_offline(newsletter.url)
        print folder_path, index_name
        time.sleep(2)
        newsletter_files = []
        index_id = None # index.html id

        for file_name in listdir(folder_path):
            file_id = fs.put(folder_path+"/"+file_name)
            newsletter_files.append(file_id)
            if file_name == index_name+".html":
                index_id = file_id
        archive.insert({
            "subject":newsletter.subject,
            "files": newsletter_files,
            "index": index_id, 
            })

        print "saving %s to mongodb" %newsletter.subject
        newsletter.saved_mongo=True
        newsletter.save()

