import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from reviews.models import Comment, Review, Title


@pytest.mark.django_db
def test_comments_cannot_be_read_or_created_under_another_title():
    user = get_user_model().objects.create_user(
        username='commenter', email='commenter@example.test'
    )
    correct_title = Title.objects.create(name='Correct', year=2020)
    other_title = Title.objects.create(name='Other', year=2021)
    review = Review.objects.create(
        title=correct_title, author=user, text='Review', score=8
    )
    comment = Comment.objects.create(review=review, author=user, text='Comment')
    wrong_url = (
        f'/api/v1/titles/{other_title.id}/reviews/{review.id}/comments/'
    )
    client = APIClient()
    client.force_authenticate(user=user)

    assert client.get(wrong_url).status_code == 404
    assert client.get(f'{wrong_url}{comment.id}/').status_code == 404
    assert client.post(wrong_url, {'text': 'Wrong title'}).status_code == 404
    assert Comment.objects.filter(review=review).count() == 1


@pytest.mark.django_db
def test_reviews_for_missing_title_return_not_found():
    client = APIClient()
    assert client.get('/api/v1/titles/999999/reviews/').status_code == 404
