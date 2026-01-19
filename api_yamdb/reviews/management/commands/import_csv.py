import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User 

class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов'

    def handle(self, *args, **options):
        data_path = os.path.join(settings.BASE_DIR, 'static/data/')

        # ВАЖНО: Порядок импорта имеет значение!
        
        # 1. Пользователи
        with open(os.path.join(data_path, 'users.csv'), encoding='utf-8') as f:
            for row in csv.DictReader(f):
                User.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'username': row['username'],
                        'email': row['email'],
                        'role': row['role'],
                        'bio': row.get('bio', ''),
                        'first_name': row.get('first_name', ''),
                        'last_name': row.get('last_name', ''),
                    }
                )
        self.stdout.write(self.style.SUCCESS('Пользователи импортированы'))

        # 2. Категории (СНАЧАЛА КАТЕГОРИИ!)
        with open(os.path.join(data_path, 'category.csv'), encoding='utf-8') as f:
            for row in csv.DictReader(f):
                Category.objects.get_or_create(
                    id=row['id'],
                    defaults={'name': row['name'], 'slug': row['slug']}
                )
        self.stdout.write(self.style.SUCCESS('Категории импортированы'))

        # 3. Жанры
        with open(os.path.join(data_path, 'genre.csv'), encoding='utf-8') as f:
            for row in csv.DictReader(f):
                Genre.objects.get_or_create(
                    id=row['id'],
                    defaults={'name': row['name'], 'slug': row['slug']}
                )
        self.stdout.write(self.style.SUCCESS('Жанры импортированы'))

        # 4. Произведения (Теперь они найдут свои категории)
        with open(os.path.join(data_path, 'titles.csv'), encoding='utf-8') as f:
            for row in csv.DictReader(f):
                category = Category.objects.get(id=row['category'])
                Title.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'year': row['year'],
                        'category': category
                    }
                )
        self.stdout.write(self.style.SUCCESS('Произведения импортированы'))

        # 5. Связи Жанров и Произведений
        with open(os.path.join(data_path, 'genre_title.csv'), encoding='utf-8') as f:
            for row in csv.DictReader(f):
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
        self.stdout.write(self.style.SUCCESS('Связи жанров импортированы'))

        # 6. Отзывы
        with open(os.path.join(data_path, 'review.csv'), encoding='utf-8') as f:
            for row in csv.DictReader(f):
                Review.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'title_id': row['title_id'],
                        'text': row['text'],
                        'author_id': row['author'],
                        'score': row['score'],
                        'pub_date': row['pub_date']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Отзывы импортированы'))

        # 7. Комментарии
        with open(os.path.join(data_path, 'comments.csv'), encoding='utf-8') as f:
            for row in csv.DictReader(f):
                Comment.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'review_id': row['review_id'],
                        'text': row['text'],
                        'author_id': row['author'],
                        'pub_date': row['pub_date']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Комментарии импортированы'))