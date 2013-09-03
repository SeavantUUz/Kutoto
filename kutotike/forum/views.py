# Create your views here.
# coding:utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from models import Topic,Tag
from forms import NewPostForm
from django.shortcuts import render_to_response,get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.models import User

def index(request,template_name="index.html"):
    args = {}
    args['topics'] = Topic.objects.all().order_by('-latest_replied_time')
    return render(request,template_name,args)



## It is no need to distinct new_topic
## and new_post.Only to seed a topic_id
##def new_post(request,topic_id,

def new_post(request,tid=0,posted_by=1,template_name='post.html'):
    c = {}
    c.update(csrf(request))
    tag = get_object_or_404(Tag,pk=1)
    user = get_object_or_404(User,pk=1)
    if tid:
        tid = int(tid)
        topic = get_object_or_404(Topic,pk=tid)
    else:
        topic=None
    if request.method == "POST":
        f = NewPostForm(request.POST,topic=topic,tag=tag,user=user)
        if f.is_valid():
            post = f.save()
    else:
        f = NewPostForm(topic=topic)
    c['form'] = f
    return render_to_response('post.html',c)

def show_post(request,tid=1):
    tid = int(tid) 
    topic = get_object_or_404(Topic,pk=tid)
    results = topic.post_set.all()
    posts = {}
    posts['posts'] = results
    return render_to_response('show_content.html',posts)

def delete_topic(request,tid=1):
    topic = get_object_or_404(Topic,pk=tid)
    tag = topic.tag
    topic.delete()
    tag.tag_update()
    return HttpResponseRedirect(reverse(index))
