from django.shortcuts import render,get_object_or_404
from .models import Post, Comment
from authuser.models import Members
from actions.models import Actions
from django.contrib.auth import get_user_model
from .forms import CommentForm, PostAddForm, SearchForm, ProfileEditForm, PostEditForm
import random
from authuser.forms import CustomUserForm
from actions.utils import create_action
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, \
PageNotAnInteger
 #Create your views here.
 
User=get_user_model()

def landing_page(request): 
    pass

@login_required
def home(request, for_you=None):
    
    #contains list of posts for various users
    #For You Page
    #first we check the trending hashtags by checking the if the occurence of a tag in several posts
    #Second we check user's most interactive session with a post(likes or Views or Comments-- having all three increases the rank)and reveal more posts from that author
    #Third we check a current view post if liked or commented on we reveal similar posts by checking the contents of such posts this happens only in a singular session
    posts={
            "For You":[],
            "Following":[]
            }
    user=request.user
    user_object=User.objects.filter(username=user.username)
    likedposts=user.liked_posts.values_list("id",flat=True)
    views=user_object.annotate(most_views=Count("views")).order_by("-most_views")
    likes=user_object.annotate(most_likes=Count("liked_posts")).order_by("-most_likes")
    users_following_posts_id=list(user.userprofile.following.values_list('id',flat=True))
    if for_you:
        trending_hashtags=Post.trending_posts().values_list("id",flat=True)
        users_favourite_posts_id=list(user.userprofile.favorites.values_list('id',flat=True))
        total=users_following_posts_id+users_favourite_posts_id
        posts["For You"]=posts=Post.published.filter(
                                                        author_id__in=total,id__in=trending_hashtags
                                                        ).exclude(id__in=likedposts)
                                                       
                                                      
    else:
        posts["Following"]=posts=Post.published.filter(
                                                            author_id__in=users_following_posts_id
                                                            ) .exclude(id__in=likedposts)
                                                            
    return render(request,"home.html",{"posts":posts})
    ''' Search online for an algorithm on who to follow'''
   # paginator=Paginator(posts,20)
#    page=request.GET.get("page")
#    try:
#        posts=paginator.page(page)
#    except PageNotAnInteger:
#        posts=paginator.page(1)
#    except EmptyPage:
#        posts=paginator.page(paginator.num_pages)
#    return posts
#    
        
@login_required              
def post_details(request,post_id):
    post=get_object_or_404(Post,id=id, status=Post.status.Published)
    views=post.views.add(request.user) if request.user not in post.views.all() else ""
    comments=post.comments.all().filter(active=True)
    form=CommentForm()
    #add
    #search body of post and using a search algorithm to find similar posts to add to user's fyp
    #and add to the current user favorites
    return render (request,"",{"comments": comments,"form":form,"post":post})   
        
        
        
@login_required
def comment_details(request,id):
        comment=get_object_or_404(Comment, id=id)
        replies=comment.comment_replies()
        form=CommentForm()
        return render(request,"",{"comment":comment,"replies": replies,"form":form})
        
#Use AJAX
@login_required
@require_POST
def post_comment(request):
    post_id=request.POST.get("id")
    action=request.POST.get("action")
    comment=request.POST.get("comment")
    if post_id and action:
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        if action=="add":
            post.comments.add()
            comment.post = post
            comment.save()
            return JsonResponse ({"comment": comment.post})
        else:
            pass
    return JsonResponse({"status":"error"})
     
      
       
         
@login_required
def profile(request):
    user_profile=request.user.userprofile
    user_posts=request.user.posts.all().filter(active=True)
    return render (request,"",{"user":user_profile,"posts":user_posts})
    




@login_required
def edit_profile(request):
    form=ProfileEditForm(instance=request.user.userprofile)
    user=CustomUserEditForm(instance=request.user)
    if request.method=="POST":
        profile_form=ProfileEditForm(instance=request.user.userprofile,data=request.POST)
        user_form=CustomUserEditForm(instance=request.user,data=request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
    else:
        return JsonResponse ({"status":"error"})
    return render (request,"",{"profile_form": profile_form,"user_form":user_form})
        
        



@login_required
def make_post(request):
    if request.method =="POST":
        form=PostForm(data=request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            create_action(request.user,"created a new post",post)
    else:
        form=PostForm()
    return render (request,"",{"form":form})




@login_required
def edit_post(request,id):
    post=get_object_or_404(Post, id=id)
    if request.method=="POST":
        post_form=PostEditForm(instance=post,data=request.POST)
        if post_form.is_valid():
            post_form.save()
    else:
        form=PostEditForm(instance=post)
    return render (request,"",{"post_form": post_form})
        




#use Ajax
#install PostgreSQL
#but first let me use the one that supports SQLite
def search(request):
    query=request.POST.get("query") or request.GET.get("query")
    if query:
        pass
        
        
        
    

@login_required
@require_POST
def like_posts(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.published.get(id=post_id)
            if action == 'like':
                post.likes.add(request.user)
                return JsonResponse ({"status":"like"})
            else:
                post.likes.remove(request.user)
                return JsonResponse({'status': 'unlike'})
        except Post.DoesNotExist:
                pass 
    return JsonResponse({'status': 'error'})






@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Members.objects.get_or_create(user1=request.user,user2=user)
                return JsonResponse ({"status":"follow"})
            else:
                Members.objects.filter(user1=request.user,user2=user).delete()
                return JsonResponse({'status':'unfollow'})
        except User.DoesNotExist:
            pass
    return JsonResponse({'status':'error'})
# add permission so only user can view it






@login_required
@require_POST
def savepost(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post= Post.published.get(id=post_id)
            if action == 'save':
                user=UserProfile.objects.get(user=request.user)
                user.saved_posts.add(post)
                return JsonResponse({'status':'saved'})
            else:
                user=UserProfile.objects.filter(user=request.user)
                user.saved_posts.remove(post)
                return JsonResponse({'status':'deleted'})
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status':'error'})



