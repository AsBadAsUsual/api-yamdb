from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (APIGetToken, APISignup, TitleViewSet, CategoryViewSet,
                    GenreViewSet)


router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")

urlpatterns = [
    path("v1/", include(router.urls)),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
