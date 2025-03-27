from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import os
from dotenv import load_dotenv


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

class LoginView(APIView):
    def post(self, request):
        email=request.data.get('email')
        password=request.data.get('password')
        
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user=authenticate(email=email, password=password)
        if not user:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        access_token = str(RefreshToken.for_user(user).access_token)
        refresh_token = str(RefreshToken.for_user(user))
        
        return Response({"message": "Login successful",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": user.email}, status=status.HTTP_200_OK)
        
        
        
        

        
class RegisterUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        image = request.data.get('image')
        print(image, "IMAGE")
        
        # Validate required fields
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not image:
            return Response({"error": "Profile image is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Validate password using Django's built-in validators
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        
        
        try:
            # Upload image to Cloudinary
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result['secure_url']
            
            # Create user with image
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                image=image_url
            )
            
            return Response({
                "message": "Registration successful",
                "user": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "image": user.image
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": f"Failed to upload image: {str(e)}"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            
            
