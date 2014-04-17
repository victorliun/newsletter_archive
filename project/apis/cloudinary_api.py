"""
This module manage the interface of cloudinay.
More info go to.http://cloudinary.com/documentation/django_integration#getting_started_guide
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings

class CloudinaryAPI():
    """
    API for cloudinary:
    This class provide a way to upload image to cloudinary. And
    Get resource from cloudinay
    """

    def __init__(self):
        """
        Initialize API
        Config your cloudinary here with your cloud_name, api_key and  api_secret
        """
        self.config = cloudinary.config(**settings.CLOUDINARY_CONFIG)
        self.api = cloudinary.api
        self.uploader = cloudinary.uploader

    def upload(self, file_path, options=None):
        """
        upload images to cloudinary.
        This function takes one parameter, dictionary, and it must have a 
        """
        default_options = {
            'crop':'limit',
            'width':5000,
            'height':5000,
            'eager':[
                { 'width': 200, 'height': 200, 
                  'crop': 'thumb', 'gravity': 'face',
                  'radius': 20,},
                { 'width': 100, 'height': 150, 
                  'crop': 'fit', 'format': 'png' }
            ],                                     
            'tags':['special',]
        }
        if options:
            options = dict(list(default_options.items()) + list(options.items()))
        else:
            options = default_options

        return self.uploader.upload(file_path, **options)

    def resources(self):
        """
        return all images in the cloudinary
        """

        return self.api.resources()

    def rescoure(self, public_id):
        """
        Get resource of image with public_id provided.
        """

        return self.api.resource(public_id)

