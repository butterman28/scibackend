from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import *
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import filters,status,generics
from .models import Post, Comment
from rest_framework.decorators import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema

class postview(APIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    #serializer_class = PostSerializer
    @swagger_auto_schema(
        operation_summary="Display all post",
        operation_description="shows all post in the data base",
    )
    def get(self,request:Request,*args,**kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(instance=posts,many=True)
        return Response(data = serializer.data,status = status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_summary="Create a new post",
        operation_description="enter title and content",
    )
    def post(self,request:Request,*args,**kwargs):
        data = request.data
        user = self.request.user
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(author=user)
            response = {
                "message":"post created",
                "data":serializer.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)    

class postupdatedelete(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Get a particular post",
        operation_description="fetch only one post by appending its id at the end of the url",
    )
    def get(self,request:Request,post_id:int):
        post = get_object_or_404(Post,id=post_id)
        
        like = get_object_or_404(Like,post=post)
        serializer = self.serializer_class(instance=post)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_summary="Update a post",
        operation_description="update a particular post in the database by appending its id at the end of the url",
    )
    def put(self,request:Request,post_id:int):
        post = get_object_or_404(Post,id=post_id)
        data = request.data
        serializer = self.serializer_class(instance=post,data=data)
        user = self.request.user
        if serializer.is_valid() and user == post.author:
            serializer.save()
            response = {
                "message":"Post updated",
                "data":serializer.data
            }
            return Response(data=response,status=status.HTTP_200_OK)
        if user != post.author:
            response = {
                "message":"Not Authorized",
                "data":serializer.data
            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST) 
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)        
    @swagger_auto_schema(
        operation_summary="Delete a post",
        operation_description="delete a particular post in the database by appending its id at the end of the url",
    )
    def delete(self,request:Request,post_id:int):
        post = get_object_or_404(Post,id=post_id)
        user = self.request.user
        if user == post.author:
            post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LikeView(APIView):
    serializer_class = likeSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self,request:Request,post_id:int):
        post = get_object_or_404(Post,id=post_id)
        like = Like.objects.all()
        serializer = self.serializer_class(instance=like)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request:Request,post_id:int):
        post = get_object_or_404(Post,id=post_id)
        like = Like.objects.all()
        user = self.request.user
        data = request.data
        serializer = likeSerializer(data=request.data)
        if Like.objects.filter(post=post, user=user).exists() == False:
            #serializer.save(user=user,post=post)
            Like.objects.create(user=user,post=post)
            response = {
                "message":"liked",
                #"data":serializer.data
                }
            return Response(data=response,status=status.HTTP_200_OK)
        else:
            Like.objects.get(post=post,user=user).delete()
            response = {
                "message":"unliked",
                #"data":serializer.data
                }
            return Response(data=response,status=status.HTTP_200_OK)

# Create your views here.
class commentview(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self,request:Request,*args,**kwargs):
        post =Post.objects.all()
        #like = Like.objects.all()
        serializer = self.serializer_class(instance=post)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self,request:Request,post_id:int):
        post = get_object_or_404(Post,id= post_id)
        data = request.data
        comment = Comment.objects.all()
        user = self.request.user
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post,author=user)
            response = {
                "message":"comment created",
                "data":serializer.data
                }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class commentupdate(APIView):
    serializer_class = CommentupdateSerializer
    @swagger_auto_schema(
        operation_summary="view all post with their comments",
        #operation_description="comment on a particular post in the database by appending its id at the end of the url",
    )
    def get(self,request:Request,*args,**kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(instance=posts,many=True)
        return Response(data = serializer.data,status = status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_summary="Update A comment",
        operation_description="update a particular comment on a particular post in the database by appending its id at the end of the url http://127.0.0.1:8000/blog/commentadjust/id",
    )
    def put(self,request:Request,comment_id:int):
        comment = get_object_or_404(Comment,id=comment_id)
        data = request.data
        user = self.request.user
        serializer = CommentupdateSerializer(instance=comment, data=data)
        if serializer.is_valid() and comment.author == user:
            serializer.save()
            response = {
                "message":"comment updated",
                "data":serializer.data
            }
            return Response(data=response,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="delete a comment",
        operation_description="delete a comment on a particular post in the database by appending its id at the end of the url http://127.0.0.1:8000/blog/commentadjust/delete/id",
    )        
    def delete(self,request:Request,comment_id:int):
        comment = get_object_or_404(Comment,id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class likes(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request:Request,*args,**kwargs):
        likes = Like.objects.all()
        serializer = LikSerializer(instance=likes,many=True)
        return Response(data = serializer.data,status = status.HTTP_200_OK)
        
        