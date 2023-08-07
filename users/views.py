from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PrivateUserSerializer


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
