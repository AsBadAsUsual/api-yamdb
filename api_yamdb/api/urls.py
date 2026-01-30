from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from django.urls import include, path

from .views import APIGetToken, APISignup, TitleViewSet, CategoryViewSet, GenreViewSet, ReviewsViewSet, CommentsViewSet, UserViewSet


router = DefaultRouter()
router.register(r"titles", TitleViewSet, basename="titles")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r'users', UserViewSet, basename='users')

titles_router = routers.NestedSimpleRouter(router, r'titles', lookup='title')
titles_router.register(r'reviews', ReviewsViewSet, basename='title-reviews')

reviews_router = routers.NestedSimpleRouter(titles_router, r'reviews', lookup='review')
reviews_router.register(r'comments', CommentsViewSet, basename='review-comments')

urlpatterns = [
    path("v1/", include(router.urls)),
    path('v1/', include(titles_router.urls)),
    path('v1/', include(reviews_router.urls)),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
