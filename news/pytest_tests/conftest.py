import pytest

from django.test.client import Client
from django.utils import timezone

from news.models import News, Comment


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)  # Логиним обычного пользователя в клиенте.
    return client

@pytest.fixture
def news():
    news = News.objects.create(  # Создаём объект заметки.
        title='Заголовок',
        text='Текст новости',
    )
    return news

@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
            news=news,
            author=author,
            text='Текст комментария'
        )
    return comment

@pytest.fixture
def id_for_args(comment):
    return (comment.id,)

@pytest.fixture
def news_for_home_page():
    news_list = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=timezone.now() - timezone.timedelta(days=index),
        )
        for index in range(11)
    ]
    return News.objects.bulk_create(news_list)

@pytest.fixture
def comments_for_detail_page(news, author):
    now = timezone.now()
    comments = [
        Comment(
            news=news,
            author=author,
            text=f'Комментарий {index}',
            created=now + timezone.timedelta(days=index)
        )
        for index in range(10)
    ]
    return Comment.objects.bulk_create(comments)

@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст'
    }
