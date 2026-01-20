from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Avg

from reviews.models import Category, Genre, Title, Review, Comment


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        """Переопределяем представление для GET-запросов"""
        ret = super().to_representation(instance)
        # Для GET-запроса возвращаем полный объект категории
        ret['category'] = CategorySerializer(instance.category).data
        # Для GET-запроса возвращаем полные объекты жанров
        ret['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        # Вычисляем рейтинг как среднюю оценку отзывов
        avg_score = instance.reviews.aggregate(Avg('score'))['score__avg']
        ret['rating'] = avg_score
        return ret

    def create(self, validated_data):
        # Извлекаем genre из validated_data, так как это ManyToMany поле
        genres = validated_data.pop('genre', [])
        # Создаем объект Title без genre
        title = Title.objects.create(**validated_data)
        # Добавляем genre отдельно
        if genres:
            title.genre.set(genres)
        return title

    def update(self, instance, validated_data):
        # Извлекаем genre из validated_data, так как это ManyToMany поле
        genres = validated_data.pop('genre', None)
        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Обновляем genre если оно было передано
        if genres is not None:
            instance.genre.set(genres)
        return instance
        

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'pub_date')

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10.')
        return value

    def validate(self, data):
        # Проверяем, не существует ли уже отзыв от этого пользователя на это произведение
        # Только при создании нового отзыва (POST), не при обновлении (PATCH)
        if self.instance is None:  # self.instance is None означает создание, а не обновление
            request = self.context.get('request')
            title_id = self.context.get('view').kwargs.get('title_pk')
            
            if request and title_id:
                existing_review = Review.objects.filter(
                    title_id=title_id,
                    author=request.user
                ).exists()
                
                if existing_review:
                    raise serializers.ValidationError(
                        'У вас уже есть отзыв на это произведение.'
                    )
        
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date')


#class ConfirmationCodeSerializer(serializers.Serializer):
#    username = serializers.CharField(max_length=150)
#    confirmation_code = serializers.CharField(max_length=50)
#
#
#class TokenSerializer(serializers.Serializer):
#    username = serializers.CharField(max_length=150)
#    confirmation_code = serializers.CharField(max_length=50)