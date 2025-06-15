import pytest
from http import HTTPStatus

from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf
from django.urls import reverse


@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)

@pytest.mark.django_db
def test_availability_for_anonymous_user(client, name):
    url = reverse(name)
    if name == 'users:logout':
        response = client.post(url)
    else:
        response = client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.django_db
def test_detail_availability_for_anonymous_user(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lf('reader_client'), HTTPStatus.NOT_FOUND),
        (lf('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_pages_availability_for_different_users(parametrized_client, name, comment, expected_status):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status

@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', lf('id_for_args')),
        ('news:delete', lf('id_for_args')),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
