from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_user_can_create_comment(author_client, author, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author

@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0

def test_user_cant_use_bad_words(author_client, news, form_data):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(reverse('news:detail', args=(news.id,)), data=bad_words_data)
    form = response.context['form']
    assert form.errors['text'] == [f'{WARNING}']
    assert Comment.objects.count() == 0

def test_author_can_delete_comment(author_client, comment, id_for_args):
    url = reverse('news:delete', args=id_for_args)
    response = author_client.post(url)
    assertRedirects(response, reverse('news:detail', args=(comment.news.id,)) + '#comments')
    assert Comment.objects.count() == 0

def test_user_cant_delete_comment_of_another_user(reader_client, comment, id_for_args):
    url = reverse('news:delete', args=id_for_args)
    response = reader_client.post(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1

def test_author_can_edit_comment(author_client, comment, form_data, id_for_args):
    url = reverse('news:edit', args=id_for_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, reverse('news:detail', args=(comment.news.id,)) + '#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.author == comment.author

def test_user_cant_edit_comment_of_another_user(reader_client, comment, form_data, id_for_args):
    url = reverse('news:edit', args=id_for_args)
    response = reader_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != form_data['text']
    assert comment.author == comment.author
