from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import APIGetToken, APISignup, TitleViewSet, CategoryViewSet, GenreViewSet, ReviewsViewSet, UserMeView


router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("reviews", ReviewsViewSet, basename="reviews")

urlpatterns = [
    path("v1/", include(router.urls)),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/users/me/', UserMeView.as_view(), name='me')
]
