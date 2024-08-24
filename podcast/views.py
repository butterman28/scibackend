from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework.decorators import APIView
from blog.models import (
    Podcast,
    Podcast_Comment,
    Podcast_Like,
)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from podcast.serializers import (
    PodcastSerializer,
    PodlikeSerializer,
    PodLikSerializer,
)

# from rest_framework.permissions import *
import base64
from django.core.files.base import ContentFile


class podcastview(APIView):
    queryset = Podcast.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PodcastSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    # serializer_class = PostSerializer
    @swagger_auto_schema(
        operation_summary="Display all post",
        operation_description="shows all post in the data base",
    )
    def get(self, request: Request, *args, **kwargs):
        podcast = Podcast.objects.all()
        serializer = PodcastSerializer(instance=podcast, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new post",
        operation_description="enter title and content",
    )
    def post(self, request: Request, *args, **kwargs):
        data = request.data
        user = self.request.user
        title = data.get("title")
        content = data.get("content")
        image = data.get("image")
        cat = data.get("category")
        audio = data.get("audio")
        # print(image)
        if image:
            # Decode base64 string into image data
            # format, img = image.split(';base64,')
            image_file = ContentFile(
                base64.b64decode(image),
                name="postimg.png",
            )
        if audio:
            audio_data = base64.b64decode(audio)
            audio_file = ContentFile(audio_data, name="audiofile.wav")

        if user.username != "Oluwadara Alegbeleye":
            post_data = {
                "title": title,
                "content": content,
                "image": image_file,
                "category": cat,
                "audio": audio_file,
            }
            serializer = PodcastSerializer(data=post_data)
            # print(serializer.initial_data)
            if serializer.is_valid():
                serializer.save(author=user)
                response = {"message": "post created", "data": serializer.data}
                print(serializer.data)
                return Response(data=response, status=status.HTTP_201_CREATED)
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            response = {
                "message": "Unauthorized",
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class PodcastLikeView(APIView):
    serializer_class = PodlikeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, podcast_id: int):
        #  post = get_object_or_404(Post, id=podcast_id)
        like = Podcast_Like.objects.all()
        serializer = self.serializer_class(instance=like)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, podcast_id: int):
        podcast = get_object_or_404(Podcast, id=podcast_id)
        # posts = Post.objects.all()
        # like = Like.objects.all()
        user = self.request.user
        # data = request.data
        # serializer = likeSerializer(data=request.data)
        if Podcast_Like.objects.filter(podcast=podcast, user=user).exists() is False:
            # serializer.save(user=user,post=post)
            like = Podcast_Like.objects.create(
                user=user,
                podcast=podcast,
            )
            # likes = Like.objects.get(post__id=podcast_id)
            serializerlike = PodLikSerializer(instance=like)
            print(serializerlike.data)
            response = {"message": "liked", "data": serializerlike.data}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            Podcast_Like.objects.get(podcast=podcast, user=user).delete()
            response = {
                "message": "unliked",
                # "data":serializerlike.data
            }
            print(response)
            return Response(data=response, status=status.HTTP_200_OK)


# Create your views here.
