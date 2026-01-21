from django.urls import path, include
from .auth import GetTokenByCodeView, SignUpView
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import GenreViewSet, CategoryViewSet, TitleViewSet, ReviewViewSet, CommentViewSet, UserViewSet


router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'titles', TitleViewSet, basename='title')
router.register(r'users', UserViewSet, basename='user')

# Nested routes for reviews
titles_router = routers.NestedDefaultRouter(router, r'titles', lookup='title')
titles_router.register(r'reviews', ReviewViewSet, basename='review')

# Nested routes for comments
reviews_router = routers.NestedDefaultRouter(titles_router, r'reviews', lookup='review')
reviews_router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', GetTokenByCodeView.as_view(), name='token'),
    path('', include(router.urls)),
    path('', include(titles_router.urls)),
    path('', include(reviews_router.urls)),
]
