"""
This models define necessary tasks for this app. 
"""

#from celery.task.schedules import crontab  
from celery.task import task
from celery.decorators import periodic_task
from apps.archive.utils import *
# this will run every minute
#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
#@task
#def test():
#    print "firing this task"

get_newsletters=task(get_newsletters)
get_images=task(save_newsletter_screenshot)
upload_images=task(upload_images_to_cloudinary)
mv_newsletters=task(mv_reviewed_newsletter)
save_offline_newsletter_to_mongodb=task(save_offline_newsletter_to_mongodb)