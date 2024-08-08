from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserViewSet, RigisterView, CustomTokenObtainPairView, RegisterAdminView, UpdatePasswordView, UpdateAdminPasswordView, VerifyEmailView, AdminAuthorAll
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
router = DefaultRouter()

router.register(r'custom-admin', RegisterAdminView, basename='create-admin')
router.register(r'user', UserViewSet, basename='UserViewSet')
router.register(r'role', RoleViewSet, basename='create-role')
router.register(r'admin/author-all',AdminAuthorAll,basename='admin-author-all')
urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RigisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('update-author-password/<pk>/', UpdatePasswordView.as_view(), name='update_password'),
    path('update-admin-password/<pk>/', UpdateAdminPasswordView.as_view(), name='update_password'),
    path('', include(router.urls)),
]