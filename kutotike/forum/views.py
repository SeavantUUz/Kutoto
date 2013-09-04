# Create your views here.
# coding:utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from models import Topic,Tag
from forms import NewPostForm,EditPostForm
from django.shortcuts import render_to_response,get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.models import User

def index(request,template_name="index.html"):
    ''' This function would generate the index page
        which just list all of topics'''
    args = {}
    args['topics'] = Topic.objects.all().order_by('-latest_replied_time')
    return render(request,template_name,args)

def new_post(request,tid=0,posted_by=1,template_name='post.html'):
    ''' This function would create a new topic or
        create a replied-post.
        It depends on whether a tid was passed '''
    args = {}
    args.update(csrf(request))
    # Using default Tag
    # If you want change the Tag 
    # you should rewrite you urls
    # or add a choices-box 
    tag = get_object_or_404(Tag,pk=1)
    user = get_object_or_404(User,pk=1)
    # reply
    if tid:
        topic = get_object_or_404(Topic,pk=tid)
    # new topic
    else:
        topic=None
    if request.method == "POST":
        f = NewPostForm(request.POST,topic=topic,tag=tag,user=user)
        if f.is_valid():
            post = f.save()
        return HttpResponseRedirect(reverse(index))
    else:
        f = NewPostForm(topic=topic)
    args['form'] = f
    return render_to_response('post.html',args)

def list_posts(request,tid=0):
    if tid:
        tid = int(tid) 
        topic = get_object_or_404(Topic,pk=tid)
        results = topic.post_set.all().order_by('created_time')
        posts = {}
        posts['posts'] = results
        return render_to_response('show_content.html',posts)
    else:
        return HttpResponseRedirect(reverse(index))


def delete_topic(request,tid=0):
    if tid:
        topic = get_object_or_404(Topic,pk=tid)
        tag = topic.tag
        topic.delete()
        tag.tag_update()
        return HttpResponseRedirect(reverse(index))
    else:
        return HttpResponseRedirect(reverse(index))

def delete_post(request,tid=0,pid=0):
    if tid and pid:
        topic = get_object_or_404(Topic,pk=tid)
        post = get_object_or_404(Post,pk=pid)
        tag = topic.tag
        post.delete()
        tag.tag_update()
        return HttpResponseRedirect(reverse(index))
    else:
        return HttpResponseRedirect(reverse(index))


def edit_post(request,tid=0,pid=0):
    tag = get_object_or_404(Tag,pk=1)
    user = get_object_or_404(User,pk=1)
    topic = get_object_or_404(Topic,pk=tid)
    post = get_object_or_404(Post,pk=pid)
    if request.method == "POST":
        f = EditPostForm(request.POST,topic=topic,post=post,user = user)
        if f.is_valid():
            edit_post = f.save()
            ##return HttpResponseRedirect('../')
        return HttpResponseRedirect(reverse(index))
    else:
        f = EditPostForm(post=post,topic=topic)
    args = {}
    args.update(csrf(request))
    args['form'] = f
    return render_to_response('post.html',args)
    
