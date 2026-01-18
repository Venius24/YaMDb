from django.urls import path, include
from .auth import GetTokenByCodeView, SignUpView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', include('apps.users.urls'), basename='user')

urlpatterns = [
    path('', include('router.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', GetTokenByCodeView.as_view(), name='token_by_code'),
]
