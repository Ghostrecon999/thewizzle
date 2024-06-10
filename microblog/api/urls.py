from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'api'
router = routers.DefaultRouter()
router.register('posts', views.PostViewSet)
urlpatterns = [
        path('', include(router.urls)),
        #path('posts/',views.PostList.as_view(),name="post_list"),
        # path('posts/<pk>/',views.PostDetail.as_view(),name="post_detail"),
        ]