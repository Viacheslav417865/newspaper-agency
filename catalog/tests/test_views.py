from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from catalog.models import Topic, Newspaper, Redactor
import datetime

TOPIC_LIST_URL = reverse("catalog:topic-list")
NEWSPAPER_LIST_URL = reverse("catalog:newspaper-list")
REDACTOR_LIST_URL = reverse("catalog:redactor-list")


class PublicTopicTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(TOPIC_LIST_URL)
        self.assertEqual(response.status_code, 302)


class PrivateTopicTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_topic(self):
        Topic.objects.create(name="test1")
        Topic.objects.create(name="test2")

        response = self.client.get(TOPIC_LIST_URL)
        topics = Topic.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topic_list"]),
            list(topics),
        )
        self.assertTemplateUsed(response, "catalog/topic_list.html")


class PublicNewspaperTests(TestCase):
    def test_newspaper_list_page_login_required(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_newspaper_detail_page_login_required(self):
        url = reverse("catalog:newspaper-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class PrivateNewspaperTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Teat134test",
        )
        redactor = self.user
        topic = Topic.objects.create(name="test")
        self.newspaper = Newspaper.objects.create(
            title="test",
            content="text test",
            published_date="2021-10-10",
            topic=topic,
        )
        self.newspaper.redactors.add(redactor)
        self.client.force_login(self.user)

    def test_newspaper_list_retrieve(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        newspaper = Newspaper.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["newspaper_list"]),
            list(newspaper),
        )
        self.assertTemplateUsed(response, "catalog/newspaper_list.html")


class PublicRedactorTests(TestCase):
    def test_redactor_list_page_login_required(self):
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_redactor_detail_page_login_required(self):
        url = reverse("catalog:redactor-detail", args=[1])
        response = self.client.get(url)



class PrivateRedactorTest(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create_user(
            username="test_redactor",
            password="testpassword",
            first_name="Test",
            last_name="Redactor",
            years_of_experience=5
        )
        self.client.force_login(self.redactor)

    def test_redactor_list_retrieve(self):
        response = self.client.get(REDACTOR_LIST_URL)
        redactor = Redactor.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["redactor_list"]),
            list(redactor),
        )
        self.assertTemplateUsed(
            response,
            "catalog/redactor_list.html")

    def test_redactor_detail_retrieve(self):
        url = reverse("catalog:redactor-detail", kwargs={"pk": self.redactor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
