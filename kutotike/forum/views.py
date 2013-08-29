# Create your views here.
# coding:utf-8
from django.shortcuts import render, get_object_or_404
from models import Topic

def index(request,template_name="index.html"):
    args = {}
    args['topics'] = Topic.objects.all().order_by('-latest_replied_time')
    return render(request,template_name,args)

## It is no need to distinct new_topic
## and new_post.Only to seed a topic_id
##def new_post(request,topic_id,
