from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomDetailSerializer, RoomListSerializer
from bookings.models import Booking
from bookings.serializers import RoomBookingSerializer, PublicBookingSerializer
from categories.models import Category
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        category_pk = request.data.get("category")
        if not category_pk:
            raise ParseError("Category is required.")

        try:
            category = Category.objects.get(pk=category_pk)
            if category.category_kind != Category.CategoryKindChoices.ROOMS:
                raise ParseError("The category kind should be 'rooms'.")
        except Category.DoesNotExist:
            raise ParseError("Such category does not exist.")

        try:
            with transaction.atomic():
                new_room = serializer.save(
                    owner=request.user,
                    category=category,
                )
                amenity_pks = request.data.get("amenities")
                for amenity_pk in amenity_pks:
                    amenity = Amenity.objects.get(pk=amenity_pk)
                    new_room.amenities.add(amenity)
                serializer = RoomDetailSerializer(
                    new_room,
                    context={"request": request},
                )
                return Response(serializer.data)
        except Exception:
            raise ParseError("Such amenity does not exist.")


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)

        updated_room = serializer.save()

        category_pk = request.data.get("category")
        if category_pk:
            try:
                category = Category.objects.get(pk=category_pk)
                if category.category_kind != Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be 'rooms'.")
                updated_room = serializer.save(category=category)
            except Category.DoesNotExist:
                raise ParseError("Such category does not exist.")

        amenity_pks = request.data.get("amenities")
        if amenity_pks:
            updated_room.amenities.clear()
            for amenity_pk in amenity_pks:
                try:
                    amenity = Amenity.objects.get(pk=amenity_pk)
                    updated_room.amenities.add(amenity)
                except Amenity.DoesNotExist:
                    raise ParseError(
                        f"The amenity with id {amenity_pk} does not exist."
                    )

        serializer = RoomDetailSerializer(
            updated_room,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", "1"))
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        serializr = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializr.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        new_review = serializer.save(
            user=request.user,
            room=self.get_object(pk),
        )
        serializer = ReviewSerializer(new_review)
        return Response(serializer.data)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        new_photo = serializer.save(room=room)
        serializer = PhotoSerializer(new_photo)
        return Response(serializer.data)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", "1"))
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        serializr = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializr.data)


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            booking_kind=Booking.BookingKindChoices.ROOM,
            room_check_in__gt=now,
        )
        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomBookingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_booking = serializer.save(
            room=room,
            user=request.user,
            booking_kind=Booking.BookingKindChoices.ROOM,
        )
        serializer = PublicBookingSerializer(new_booking)
        return Response(serializer.data)


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_amenity = serializer.save()
        serializer = AmenitySerializer(new_amenity)
        return Response(serializer.data)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        updated_amenity = serializer.save()
        serializer = AmenitySerializer(updated_amenity)
        return Response(serializer.data)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
