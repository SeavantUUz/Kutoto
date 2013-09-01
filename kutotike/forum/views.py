# Create your views here.
# coding:utf-8
from django.shortcuts import render, get_object_or_404
from models import Topic
from forms import NewPostForm
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

def index(request,template_name="index.html"):
    args = {}
    args['topics'] = Topic.objects.all().order_by('-latest_replied_time')
    return render(request,template_name,args)



## It is no need to distinct new_topic
## and new_post.Only to seed a topic_id
##def new_post(request,topic_id,

def new_post(request):
    print request.method
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        f = NewPostForm(request.POST)
        print 'form'
        if f.is_valid():
            cd = f.cleaned_data
            for k in cd:
                print k,cd[k]
    else:
        f = NewPostForm()
    c['form'] = f
    return render_to_response('post.html',c)
