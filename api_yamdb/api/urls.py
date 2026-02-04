from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from api.views import (
    APIGetToken,
    APISignup,
    CategoryViewSet,
    CommentsViewSet,
    GenreViewSet,
    ReviewsViewSet,
    TitleViewSet,
    UserViewSet,
)

router_v1 = DefaultRouter()
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register("categories", CategoryViewSet, basename="categories")
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register("users", UserViewSet, basename="users")

titles_router = routers.NestedSimpleRouter(
    router_v1, r"titles", lookup="title"
)
titles_router.register(r"reviews", ReviewsViewSet, basename="title-reviews")

reviews_router = routers.NestedSimpleRouter(
    titles_router, r"reviews", lookup="review"
)
reviews_router.register(
    r"comments", CommentsViewSet, basename="review-comments"
)

urlpatterns_auth = [
    path("token/", APIGetToken.as_view(), name="get_token"),
    path("signup/", APISignup.as_view(), name="signup"),
]

urlpatterns_v1 = [
    path("auth/", include(urlpatterns_auth)),
    path("", include(router_v1.urls)),
    path("", include(titles_router.urls)),
    path("", include(reviews_router.urls)),
]

urlpatterns = [path("v1/", include(urlpatterns_v1))]
