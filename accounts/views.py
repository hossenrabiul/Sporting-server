from django.shortcuts import render,redirect
from rest_framework import viewsets, status
from . import serializers
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    print('hey ia mhere')
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"https://sporting-server-xi.vercel.app/accounts/active/{uid}/{token}/"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('comfirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({"message": "Check your email to confirm your account."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate(request,uid64,token):
    print("hello word")

    try:
        uid = urlsafe_base64_decode(uid64).decode()
        print("uid", uid)
        user = User._default_manager.get(pk=uid)
        print("use", user)
    except (User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True 
        user.save()
     
        return redirect('login')
    else:
        
        return redirect('register')
    

# # class UserLoginApiView(APIView):
#     def post(self, request):
#         serializer = serializers.UserLoginSerializer(data = self.request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']

#             user = authenticate(username= username, password=password)
            
#             if user:
#                 token, _ = Token.objects.get_or_create(user=user)
#                 print(token)
#                 print(_)
#                 login(request, user)
#                 return Response({'token' : token.key, 'user_id' : user.id})
#             else:
#                 return Response({'error' : "Invalid Credential"})
#         return Response(serializer.errors)


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print("token"  ,token, "req"  ,request)
                login(request, user)
                
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'is_superuser': user.is_superuser, # ✅ Include admin status
                    'username' : username,
                    'password' : password
                })
            else:
                return Response({'error': "Invalid Credential"}, status=400)

        return Response(serializer.errors, status=400)


class userProfileUpdateView(RetrieveUpdateAPIView):
    querysetj = User.objects.all()
    serializer_class = serializers.userProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserLogoutView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response({"message": "Successfully logged out"}, status=200)
        else:
            return Response({"error": "User is not authenticated"}, status=400)
    

    
class userProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.userSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ContactView(APIView):

    def post(self, request):
        serializer = serializers.ContactSerializer(data=request.data)
        
        if serializer.is_valid():
            # Send the email
            serializer.send_email()
            return Response({"message": "Your message has been sent successfully!"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

