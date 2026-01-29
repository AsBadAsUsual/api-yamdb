from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import APIGetToken, APISignup, TitleViewSet, CategoryViewSet, GenreViewSet, ReviewsViewSet, CommentsViewSet, UserMeView


router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles/(?P<title_id>[^/.]+)/reviews", ReviewsViewSet, basename="reviews")
router.register("titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments/", CommentsViewSet, basename="comments")

urlpatterns = [
    path("v1/", include(router.urls)),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/users/me/', UserMeView.as_view(), name='me')
]
