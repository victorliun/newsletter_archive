from django.core.management.base import BaseCommand, CommandError
from apps.archive.utils import save_newsletter_screenshot

class Command(BaseCommand):
    help = """
        Get image from phantom js. This command will sender newsletters with status 1, 
        send url to phantomjs and save image local.
        """

    def handle(self, *args, **options):
        """
        Call function: 
        """
        
        save_newsletter_screenshot()
