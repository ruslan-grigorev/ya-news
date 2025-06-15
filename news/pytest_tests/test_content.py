import pytest
from django.urls import reverse
from django.conf import settings

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(news_for_home_page, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE

@pytest.mark.django_db
def test_news_order(news_for_home_page, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = list(response.context['object_list'])

    object_dates = [news.date for news in object_list]
    expected_dates = sorted(object_dates, reverse=True)

    assert object_dates == expected_dates

@pytest.mark.django_db
def test_comments_order(news, client, comments_for_detail_page):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'news' in response.context

    news_from_context = response.context['news']
    all_comments = news_from_context.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps

def test_authorized_client_has_form(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    # Запрашиваем страницу создания заметки:
    response = author_client.get(url)
    # Проверяем, есть ли объект form в словаре контекста:
    assert 'form' in response.context
    # Проверяем, что объект формы относится к нужному классу.
    assert isinstance(response.context['form'], CommentForm)

@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context
