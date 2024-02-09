from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly    
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from .models import Photo
from .serializers import PhotoSerializer, PhotoDetailSerializer


class Photos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_photos = Photo.objects.all()
        serializer = PhotoSerializer(
            all_photos,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_photo = serializer.save()
        serializer = PhotoSerializer(new_photo)
        return Response(serializer.data)


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        photo = self.get_object(pk)
        serializer = PhotoDetailSerializer(
            photo,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if photo.room and photo.room.owner != request.user:
            raise PermissionDenied

        photo.delete()
        return Response(status=HTTP_200_OK)
    