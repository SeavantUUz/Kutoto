# coding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    '''user account'''
    user = models.OneToOneField(User,related_name='user_profile',verbose_name=u'用户')
    birthday = models.DateField(verbose_name=u'生日',blank=True)
    point = models.IntegerField(default=0,verbose_name=u'积分')
    signature = models.CharField(max_length=1000,blank=True,verbose_name='签名')
    def __unicode__(self):
        return self.user.username

    # The post_set refer that one post class
    # and get all the items from database
    def get_total_posts(self):
        return self.user.post_set.count()

    def get_absolute_url(self):
        return self.user.get_absolute_url()

class Parents_Tag(models.Model):
    name = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

## no manytomany,only onetoone
class Tag(models.Model):
    parents_tag = models.ForeignKey(Parents_Tag)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110)
    create_time = models.DateTimeField(auto_now_add=True)
    num_topics = models.IntegerField(default=0,editable=False)
    num_posts = models.IntegerField(default=0,editable=False)

    class Meta:
        ordering = ['create_time']

    def __unicode__(self):
        names = [self.parents_tag.name,self.name]
        return u'->'.join(names)

    def _get_num_topics(self):
        return self.topic_set.all().count()

    def _get_num_posts(self):
        return self.post_set.all().count()

    def tag_update(self):
        self.num_posts = self._get_num_posts()
        self.num_topics = self._get_num_topics()
        self.save()



class Topic(models.Model):
    tag = models.ForeignKey(Tag,verbose_name=u'标签')
    subject = models.CharField(max_length=1000,verbose_name=u'帖子标题')
    posted_by = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    latest_replied_time = models.DateTimeField(auto_now_add=True)
    num_replies = models.PositiveIntegerField(default=0,editable=False)

    class Meta:
        ordering = ['-created_time','-latest_replied_time']

    def __unicode__(self):
        return self.subject


class Post(models.Model):
    topic = models.ForeignKey(Topic,verbose_name=u'话题')
    tag = models.ForeignKey(Tag,verbose_name=u'标签')
    posted_by = models.ForeignKey(User)
    poster_ip = models.IPAddressField(blank=True)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if len(self.content)>=50:
            return self.content[:50]+'...'
        else:
            return self.content

    class Meta:
        ordering=['-created_time']
