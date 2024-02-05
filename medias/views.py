from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
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


class PhotoUpload(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = PhotoSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=HTTP_400_BAD_REQUEST)