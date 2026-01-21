from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import django_filters.rest_framework

from .serializers import GenreSerializer, CategorySerializer, TitleSerializer, ReviewSerializer, CommentSerializer, UserSerializer
from reviews.models import Genre, Category, Title, Review, Comment
from .permissions import IsAdminOrReadOnly, IsAdminModeratorOwnerOrReadOnly, IsStaffOrReadOnly, IsAdmin
from .filters import TitleFilter


User = get_user_model()


class ListCreateDestroyViewSet(mixins.ListModelMixin, 
                                mixins.CreateModelMixin,
                                mixins.DestroyModelMixin, 
                                viewsets.GenericViewSet):
    pass



class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug' 
    
    # Для YaMDb обычно запрещают метод PUT, оставляя только GET, POST и DELETE
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title_id = self.kwargs.get('title_pk')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_pk')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review_id = self.kwargs.get('review_pk')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_pk')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class UserPagination(PageNumberPagination):
    page_size = 10

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = UserPagination
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = [IsAdmin,]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Для PATCH
        serializer = self.get_serializer(
            user, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        # Важно: не даем менять роль через /me/
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)