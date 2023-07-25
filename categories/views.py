from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer


class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(
            all_categories,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_category = serializer.save()
        serializer = CategorySerializer(new_category)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_category = serializer.save()
        serializer = CategorySerializer(updated_category)
        return Response(serializer.data)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
