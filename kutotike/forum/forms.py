from django import forms
from models import Topic,Post

class PostForm(forms.ModelForm):
    subject = forms.CharField(label=u'主题',widget = forms.TextInput(attrs={'size':'80'}})
    content = forms.CharField(label=u'内容',widget = forms.Textarea(attrs={'cols':'95','rows':'14'}})

    class Meta:
        # use Post model
        model = Post
        ## only use message field in the model
        fields = ('content',)

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user',u'阿卡林')
        self.ip = kwargs.pop('ip',u'火星ip')
        self.topic = kwargs.pop('topic',None)
        self.tag = kwargs.pop('tag',None)
        super(PostForm,self).__init__(*args,**kwargs)

class NewPostForm(PostForm):
    def __init__(self,*args,**kwargs):
        super(NewPostForm,self).__init__(*args,**kwargs)
        ## not a new topic
        if self.topic:
            ## could not input subject
            self.fields['subject'].required = False

    def save(self):
        if not self.topic:
            ## caution I maybe will modified the name to
            ## tag in the future
            topic = Topic(tags = self.tag,
                    subject = self.cleaned_data['subject'],
                    posted_by = self.user,
                    )
            topic.save()
        else:
            topic = self.topic

        post = Post(topic=topic,posted_by=self.user,poster_ip=self.ip,content = self.cleaned_data['message'])
        post.save()
        return post

