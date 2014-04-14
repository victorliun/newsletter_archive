from django.core.management.base import BaseCommand, CommandError
from apps.archive.utils import save_offline_newsletter_to_mongodb

class Command(BaseCommand):
    help = """
        This will command will save all newsletter which haven't saved into mongodb. 
        """

    def handle(self, *args, **options):
        """
        Call utils function
        """
        
        save_offline_newsletter_to_mongodb()
