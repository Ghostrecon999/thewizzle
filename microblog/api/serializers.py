from rest_framework import serializers
from microblog.models import Post
from taggit.serializers import TagListSerializerField,TaggitSerializer

from django.contrib.auth import get_user_model

User=get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')
    class Meta:
        model=User
        fields=["username","full_name","email"]
        
class PostSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField(read_only=True)
    author=AuthorSerializer(read_only=True)
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['views'] = instance.views.count()
        representation ["likes"]=instance.likes.count()
        return representation
    class Meta:
        model=Post
        fields=["author","body","tags","comments" ]
        