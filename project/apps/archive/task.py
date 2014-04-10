"""
This models define necessary tasks for this app. 
"""

from celery.task.schedules import crontab  
from celery.decorators import periodic_task

# this will run every minute
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def test():
    print "firing this task"

