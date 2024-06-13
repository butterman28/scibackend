from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .tokens import create_jwt_pair_for_user
from rest_framework.permissions import *
import base64

# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        print(email)
        print(password)
        #print(email,password)
        user = authenticate(email=email, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)
            with open(user.profile.image.path, 'rb') as img_file:
                image = base64.b64encode(img_file.read()).decode('utf-8')
            response = {
                "message": "Login Successfull", 
                "tokens": tokens,
                "username": user.username, 
                "email":user.email,
                "profilephoto":image,
                "age":user.profile.age,
                "date_of_birth":user.date_of_birth,
                }
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request:Request,name:str):
        profile = Profile.objects.get(username=name)
        serializer = ProfileSerializer(instance=profile,many=True)
        return Response(data = serializer.data,status = status.HTTP_200_OK)
# Create your views here.
