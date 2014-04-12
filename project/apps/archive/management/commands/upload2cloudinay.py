from django.core.management.base import BaseCommand, CommandError
from apps.archive.utils import upload_images_to_cloudinary

class Command(BaseCommand):
    help = """
        This will upload images of those newsletter with status 3 to cloudinary, recieve a cloudinary image
        url and id, save then to db, and update the status of those newsletter to status 4.
        Please config your cloudinary_id first before run this. 
        """

    def handle(self, *args, **options):
        """
        Call function: 

        """
        
        upload_images_to_cloudinary()
