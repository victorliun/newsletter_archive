from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import permalink
from django.utils.text import slugify

from treebeard.mp_tree import MP_Node

from lxml import etree

def today():
    """
    Returns a tuple of two datetime instances: the beginning of today, and the 
    end of today.
    """
    now = datetime.now()
    start = datetime.min.replace(year=now.year, month=now.month, day=now.day)
    end = (start + timedelta(days=1)) - timedelta.resolution
    return (start, end)


class EmotionQuerySet(QuerySet):
    """
    A simple ``QuerySet`` subclass which adds only one extra method,
    ``today``, which returns only those objects whose ``pub_date`` falls
    within the bounds of today.
    """

    def today(self):
        """
        Filters down to only those objects whose ``pub_date`` falls within
        the bounds of today.
        """
        return self.filter(pub_date__range=today())


class EmotionManager(models.Manager):
    """
    A simple ``Manager`` subclass which returns an ``EmotionQuerySet``
    instead of the typical ``QuerySet``.  It also includes a proxy for the extra
    ``today`` method that is provided by the ``EmotionQuerySet`` subclass.
    """
    def get_query_set(self):
        """
        Gets an ``EmotionQuerySet`` instead of a typical ``QuerySet``.
        """
        return EmotionQuerySet(self.model)
    
    def today(self):
        """
        A proxy method for the extra ``today`` method that is provided by the
        ``EmotionQuerySet`` subclass.
        """
        self.get_query_set().today()



class Emotions(models.Model):
    """
    Model of table: emotions.
    This table keep recording every emotions status that posted by every user.
    Fields include:
        slug: the readable url for each record intead of using record's intead
        pub_date: the date when this record posted.
        author: the user who posted this record.
        description: the content of this record.
        latest: Indicate that wether this is the latest post by the user.
    """
    
    slug = models.SlugField(max_length=255, blank=True, null=True)
    pub_date = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(User, related_name='emotions_author')
    description = models.TextField()
    latest = models.BooleanField(default=True)
    tags = models.ManyToManyField("Tag")

    objects = EmotionManager()

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ('-pub_date',)
        verbose_name_plural = 'Emotion'
        app_label = 'emotion_recorder'
        db_table = 'emotions'
        managed = True

    def __unicode__(self):
        """
        Returns the first 80 characters of the description, or less, if the
        description is less than 80 characters.
        """
        if len(self.description) > 80:
            description = self.description[:76] + "..."
        else:
            description = self.description

        return u"%s posted '%s' at %s" %(self.author, description,
            self.pub_date.strftime("%Y-%b-%d"))

    def save(self, **kwargs):
        """
        First this generate a string for slug field if it's null.
        Second this updates all emotions have latest=True by the same creator,
        and sets their ``latest`` field to False.
        
        Then, this simply saves the object.  Since the default for ``latest`` is
        to be set to True, it will be passed through and saved as the latest
        emotions for today by this user.
        """
        
        if not self.slug:
            self.slug = slugify(unicode(self.description))

        Emotions.objects.filter(author=self.author, latest=True).update(latest=False)
        super(Emotions, self).save(**kwargs)

    def today(self):
        """
        Determines whether this Emotions takes place today or not.
        """
        (start, end) = today()
        return self.pub_date >= start and self.pub_date <= end

    @permalink
    def get_absolute_url(self):
        """
        This method tell Django how to calculate the canonical URL for an object. And it 
        appare a string that refers to this object.
        """
        from django.core.urlresolvers import reverse
        return reverse("emotion_recorder_view", {'slug': self.slug})

    def description_size(self):
        """
        Useful only for display purposes, this designates a label of 'small',
        'medium', or 'large' to the description text size.
        """
        if len(self.description) < 120:
            return 'small'
        elif len(self.description) < 240:
            return 'medium'
        else:
            return 'large'


class Tag(MP_Node):
    """
    Model for table tag. Which stores tags for emotion post.
    Fields includes:
        Id: auto increase
        name: tag's name, Must unique.  
    """
    name = models.CharField(max_length=20, null=False, unique=True)   
    node_order_by = ['name']

    class Meta:
        verbose_name_plural = 'tag'
        app_label = 'emotion_recorder'
        db_table = 'tags'
        managed = True
    
    def __unicode__(self):
        """
        Return a string as the description of this tag.
        """
        return "Tag: %s" %self.name    