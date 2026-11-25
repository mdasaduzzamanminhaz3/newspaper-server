from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import RegistrationView, CustomLoginView,ProfileView,LogoutView
from article.views import ArticleViewSet,CategoryViewSet
from rest_framework_simplejwt.views import TokenRefreshView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

router = DefaultRouter()
router.register("articles",ArticleViewSet,basename="article")
router.register('categories',CategoryViewSet,basename='category')
urlpatterns = [
    # Authentication
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # API Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # API Router
    path("", include(router.urls)),
]