from django.urls import path
from .views import Wishlists, WishlistDetail, WishlistRoom

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>", WishlistDetail.as_view()),
    path("<int:wishlist_pk>/rooms/<int:room_pk>", WishlistRoom.as_view()),
]
