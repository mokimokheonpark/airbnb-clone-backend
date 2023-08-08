import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from .models import User
from .serializers import PrivateUserSerializer, PublicUserSerializer


class Users(APIView):
    def post(self, request):
        raw_password = request.data.get("password")
        if not raw_password:
            raise ParseError

        serializer = PrivateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        new_user = serializer.save()
        new_user.set_password(raw_password)
        new_user.save()
        serializer = PrivateUserSerializer(new_user)
        return Response(serializer.data)


class UserProfile(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


class MyProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_user = serializer.save()
        serializer = PrivateUserSerializer(updated_user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError

        user = request.user
        if not user.check_password(old_password):
            raise ParseError

        user.set_password(new_password)
        user.save()
        return Response(status=HTTP_200_OK)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if not user:
            return Response({"Error": "Wrong Username or Password"})

        login(request, user)
        return Response({"Pass": "Successfully Logged In"})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"Pass": "Successfully Logged Out"})


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if not user:
            return Response({"Error": "Wrong Username or Password"})

        token = jwt.encode(
            {"pk": user.pk},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return Response({"Token": token})
