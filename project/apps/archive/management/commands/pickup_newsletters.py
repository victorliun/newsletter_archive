from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from apps.archive.models import NewsletterArchiveWIP, CompanyDetail
from django.contrib.auth.models import User
import logging

from apis.mail_api import ZMailAPI

automator = User.objects.get_or_create(username='automator')[0]

class Command(BaseCommand):
    """
    This command will pull newsletters from an email inbox. 
    and save it to db newsletterarchivewip.
        options:
            --initial: this will walk throught to the email inbox to check newsletters
            --account: Gmail account here
            --password: the password used to login
    """
    help = 'Pick up emails from email box'
    
    option_list = BaseCommand.option_list + (
    make_option('--gmail-accout', action='store', dest='gmail_accout',
        default=None, help='gmail account to connect'),
    make_option('--password', action="store", dest="password",
        default=None, help="The password of your account"),
    make_option('--initial', action="store", dest="initial",
        default=False, help="Run first time for this account?"),
    )

    def handle(self, *args, **options):
        """
        check options. login to count
        save new newsletters
        """
        initial = options.get("initial")
        gmail_accout = options.get("gmail_accout")
        password = options.get("password")
        logging.warning(gmail_accout)
        logging.warning(password)

        try:
            api = ZMailAPI(gmail_accout,password)
        except Exception, err:
            raise CommandError(err)

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
                    added_by=automator,
                    )

                # search company if exists in our table.
                company_domain = newsletter_info['sender'][1].split('@')[1]
                company = CompanyDetail.objects.filter(domain_names__icontains=company_domain)
                if company.count() == 1:
                    newsletter.company = company[0]
                    newsletter.save()
                print "store:%s" %newsletter
