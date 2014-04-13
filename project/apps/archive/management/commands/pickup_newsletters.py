from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from apps.archive.utils import get_newsletters
import logging
from django.conf import settings

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
        initial = options.get("initial", False)
        gmail_accout = options.get("gmail_accout")
        password = options.get("password")
        logging.warning(gmail_accout)
        logging.warning(password)

        get_newsletters(gmail_accout, password, initial)