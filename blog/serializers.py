from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class SearchFormSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=100)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields =["content"]
class CommentupdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        #fields = ["username", "email", "password1", "password2"]
        fields = ["username"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        #fields = '__all__'
        fields =["title","content","comments"]
        
class likeSerializer(serializers.Serializer):
    #post = PostSerializer(many=True, read_only=True)
    #user = UserSerializer(many=True, read_only=True)
    dostring = serializers.CharField(max_length=100)
    
    
    #class Meta:
        #model = Like
        #fields = '__all__'
        #fields =["post","user"]
