from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from drf_extra_fields.fields import Base64ImageField
#from drf_extra_fields.fields import Base64ImageField
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    class Meta:
        model = Profile
        fields = ["age" , "image"]
        
    def create(self, validated_data):
        # Override the create method to handle user creation
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    profile = ProfileSerializer()    

    class Meta:
        model = User
        fields = ["email", "username", "password" , "profile"]

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        Token.objects.create(user=user)

        return user

    
class CurrentUserPostsSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, view_name="post_detail", queryset=User.objects.all()
    )
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "posts"]