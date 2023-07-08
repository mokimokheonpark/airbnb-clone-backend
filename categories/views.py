from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Category
from .serializers import CategorySerializer


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(
            all_categories,
            many=True,
        )
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_category = serializer.save()
        return Response(CategorySerializer(new_category).data)


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        a_category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        serializer = CategorySerializer(a_category)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CategorySerializer(
            a_category,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_category = serializer.save()
        return Response(CategorySerializer(updated_category).data)

    elif request.method == "DELETE":
        a_category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
