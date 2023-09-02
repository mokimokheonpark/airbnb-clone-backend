import jwt
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
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
            return Response(
                {"Error": "Invalid Username or Password"},
                status=HTTP_400_BAD_REQUEST,
            )

        login(request, user)
        return Response(
            {"Pass": "Successfully Logged In"},
            status=HTTP_200_OK,
        )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"Pass": "Successfully Logged Out"},
            status=HTTP_200_OK,
        )


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
            return Response(
                {"Error": "Invalid Username or Password"},
                status=HTTP_400_BAD_REQUEST,
            )

        token = jwt.encode(
            {"pk": user.pk},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return Response({"Token": token})


class GitHubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")

            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=c9882616a87fb7e713e1&client_secret={settings.GH_SECRET}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")

            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()

            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()

            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(request, user)
                return Response(status=HTTP_200_OK)

            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_emails[0]["email"],
                    name=user_data.get("name"),
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=HTTP_200_OK)

        except Exception:
            return Response(status=HTTP_400_BAD_REQUEST)
