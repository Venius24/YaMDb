from django.urls import path, include
from .auth import GetTokenByCodeView, SignUpView
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, CategoryViewSet, TitleViewSet, ReviewViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'titles', TitleViewSet, basename='title')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', GetTokenByCodeView.as_view(), name='token_by_code'),
]
