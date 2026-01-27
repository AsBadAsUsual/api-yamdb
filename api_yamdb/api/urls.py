from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import TitlesViewSet, TitleViewSet, CategoryViewSet, GenreViewSet


router = DefaultRouter()
router.register("titles", TitlesViewSet)
router.register(r"titles/(?P<title_id>[^/.]+)", TitleViewSet, basename="titl")
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
