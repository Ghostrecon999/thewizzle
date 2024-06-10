from django.db import models
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model 
import re
from taggit.managers import TaggableManager
from taggit.models import Tag
from django.db.models import Count

# Create your models here.



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.Published)


class Post(models.Model):


    class Status(models.TextChoices):
        Draft='DR','DRAFT'
        Published='PB','PUBLISHED'


    objects=models.Manager()
    published=PublishedManager()
    tags=TaggableManager()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    publish=models.DateTimeField(blank=True,null=True,editable=False)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.Published)
    views=models.ManyToManyField(settings.AUTH_USER_MODEL,editable=False, related_name="views")#should be a m2m field storing the user's that have viewed it
    likes=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts",editable=False)
    active=models.BooleanField(default=True)
    image=models.ImageField(upload_to='postimages/%Y/%m/%d',blank=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='posts',on_delete=models.CASCADE)
    
    

    class Meta:
        ordering=['-created']
        indexes=[models.Index(fields=['-created'],)]

    def __str__(self):
        return self.body


    def get_absolute_url(self):
        return reverse('microblog:post',
                       args=[self.id])

    def post_comments(self):
        return self.comments.all().filter(replies=None)
    
    def save(self,*args,**kwargs):
        if self.status=='PB':
            self.publish=self.created
        super().save(*args,**kwargs)
        for tag in re.findall(r"#[a-zA-Z0-9]*",self.body):
            for taggs in self.tags.names():
                if taggs not in self.body:
                    self.tags.remove(taggs)
            if tag in self.body:
                self.tags.add(tag)
                
    @staticmethod
    def trending_tags():
        popular_tags=Tag.objects.all()
        popular_tags=popular_tags.annotate(total=Count('taggit_taggeditem_items')).order_by('-total')[:5]
        return popular_tags
        
    @staticmethod
    def trending_posts():
        popular_tags_id=Post.trending_tags().values_list('id',flat=True)
        trending_posts=Post.published.all().filter(tags__in=popular_tags_id).distinct()
        return trending_posts
    
    

class Comment(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments' )
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments' )
    comment=models.TextField()
    active=models.BooleanField(default=True)
    publish=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_liked_comments",editable=False)
    views=models.IntegerField(editable=False,default=0)
    reply_to_comment=models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='replies_from_comment')
    #To handle reply filter by filter(replies=None) for all the comments 
    
    def __str__(self):
        return self.comment
    

    def comment_replies(self):
        return self.replies_from_comment.all()



    def __repr__(self):
        if self.reply_to_comment==None:
            return f"Comment {self.comment} by {self.user.username}"
        else:
            return f"reply {self.comment} by {self.user.username}"

    class Meta:
        ordering=['publish']#-reply_to_comment']
        indexes=[models.Index(fields=['publish'],)]#['-reply_to_comment']
    
    def get_absolute_url(self):
        return reverse('microblog:comment',
                       args=[self.id])

class Search(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="searches")
    word=models.CharField(max_length=250)
    date=models.DateTimeField(auto_now_add=True)
    




