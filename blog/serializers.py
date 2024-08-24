from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
import base64
from django.core.files import File
from users.models import *

User = get_user_model()


class SearchFormSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=100)


class Base64ImageField(serializers.ImageField):
    """
    A custom serializer field to convert an image file to Base64 format.
    """

    def to_representation(self, value):
        if value:
            with open(value.path, "rb") as f:
                data = f.read()
                return base64.b64encode(data).decode("utf-8")
        return None


class ProimageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Profile
        fields = ["image"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProimageSerializer(read_only=True)

    class Meta:
        model = User
        # fields = ["username", "email", "password1", "password2"]
        fields = ["username", "profile"]


class likeUserSerializer(serializers.HyperlinkedModelSerializer):
    # profile = ProimageSerializer(read_only=True)
    class Meta:
        model = User
        # fields = ["username", "email", "password1", "password2"]
        fields = ["username"]


class SearchFormSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=100)


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at"]


class LikSerializer(serializers.ModelSerializer):
    user = likeUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ["post", "user", "date_liked"]


class CommentupdateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    image = Base64ImageField(required=True)
    like = LikSerializer(many=True, read_only=True, source="get_likes")

    class Meta:
        model = Post
        # fields = '__all__'
        fields = [
            "id",
            "image",
            "title",
            "content",
            "like",
            "comments",
            "category",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            with open(instance.image.path, "rb") as img_file:
                data["image"] = base64.b64encode(img_file.read()).decode("utf-8")
        return data


class PostcreationSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)
    image = Base64ImageField(required=True)
    # like = LikSerializer(many=True, read_only=True, source='get_likes')

    class Meta:
        model = Post
        # fields = '__all__'
        fields = ["image", "title", "content"]


class likeSerializer(serializers.Serializer):
    # post = PostSerializer(many=True, read_only=True)
    # user = UserSerializer(many=True, read_only=True)
    dostring = serializers.CharField(max_length=100)

    # class Meta:
    # model = Like
    # fields = '__all__'
    # fields =["post","user"]
