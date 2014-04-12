from django.core.management.base import BaseCommand, CommandError
from apps.archive.utils import mv_reviewed_newsletter

class Command(BaseCommand):
    help = """
        This will move newsletters in status 5 and save them to newsletters publish table.
        """

    def handle(self, *args, **options):
        """
        Call function: 
        """
        
        mv_reviewed_newsletter()
