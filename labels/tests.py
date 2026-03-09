from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="strong-password-123",
        )
        self.executor = User.objects.create_user(
            username="executor",
            password="executor-password-123",
        )
        self.label = Label.objects.create(name="Bug")
        self.status = Status.objects.create(name="Новый")

    def test_label_list(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.get(reverse("labels:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bug")

    def test_label_create(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("labels:create"),
            {"name": "Feature"},
        )

        self.assertRedirects(response, reverse("labels:index"))
        self.assertTrue(Label.objects.filter(name="Feature").exists())

    def test_label_update(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("labels:update", kwargs={"pk": self.label.pk}),
            {"name": "Improvement"},
        )

        self.label.refresh_from_db()

        self.assertRedirects(response, reverse("labels:index"))
        self.assertEqual(self.label.name, "Improvement")

    def test_label_delete(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("labels:delete", kwargs={"pk": self.label.pk}),
        )

        self.assertRedirects(response, reverse("labels:index"))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_list_requires_login(self):
        response = self.client.get(reverse("labels:index"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('labels:index')}",
        )

    def test_label_create_requires_login(self):
        response = self.client.get(reverse("labels:create"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('labels:create')}",
        )

    def test_label_update_requires_login(self):
        response = self.client.get(
            reverse("labels:update", kwargs={"pk": self.label.pk}),
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('labels:update', kwargs={'pk': self.label.pk})}",
        )

    def test_label_delete_requires_login(self):
        response = self.client.get(
            reverse("labels:delete", kwargs={"pk": self.label.pk}),
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('labels:delete', kwargs={'pk': self.label.pk})}",
        )

    def test_label_cannot_delete_if_linked_to_task(self):
        task = Task.objects.create(
            name="Тестовая задача",
            description="Описание",
            status=self.status,
            author=self.user,
            executor=self.executor,
        )
        task.labels.add(self.label)

        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("labels:delete", kwargs={"pk": self.label.pk}),
        )

        self.assertRedirects(response, reverse("labels:index"))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
