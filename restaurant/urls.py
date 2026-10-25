from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import BookingViewSet, LoginView, LogoutView, MenuViewSet, RegisterView

router = DefaultRouter()
router.register('menu', MenuViewSet, basename='menu')
router.register('bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/', obtain_auth_token, name='token'),
] + router.urls
