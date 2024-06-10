
from django.urls import path
from .views import home, post_details,user_follow, search,\
like_posts, savepost,post_comment, edit_post, edit_profile,\
profile,make_post

app_name='microblog'

urlpatterns=[
        path("posts/<str:for_you>",home,name="home"),
        path("/post/<int:id>/",post_details,name="post"),
        path("/follow/",user_follow,name="follow"),
        path("/search/", search,name="search"),
        path("search/<str:word>/",search,name="search"),
        path("like/",like_posts,name="like"),
        path("save/",savepost,name="save"),
        path("savedpost/",savepost,name="save"),
        path("addcomment/",post_comment,name="addcomment"),
        #path("comment/",comment_details,name="comment"),
        path ("editpost/",edit_post,name="editpost"),
        path("editprofile/",edit_profile,name="editprofile"),
        path("profile/", profile, name="profile"),
        path("createpost/",make_post, name="createpost"),
    ]