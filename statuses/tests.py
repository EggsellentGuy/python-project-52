from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="strong-password-123",
        )
        self.status = Status.objects.create(name="In progress")

    def test_status_list(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.get(reverse("statuses:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "In progress")

    def test_status_create(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("statuses:create"),
            {"name": "Done"},
        )

        self.assertRedirects(response, reverse("statuses:index"))
        self.assertTrue(Status.objects.filter(name="Done").exists())

    def test_status_update(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("statuses:update", kwargs={"pk": self.status.pk}),
            {"name": "Done"},
        )

        self.status.refresh_from_db()

        self.assertRedirects(response, reverse("statuses:index"))
        self.assertEqual(self.status.name, "Done")

    def test_status_delete(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("statuses:delete", kwargs={"pk": self.status.pk}),
        )

        self.assertRedirects(response, reverse("statuses:index"))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_status_list_requires_login(self):
        response = self.client.get(reverse("statuses:index"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('statuses:index')}",
        )

    def test_status_create_requires_login(self):
        response = self.client.get(reverse("statuses:create"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('statuses:create')}",
        )

    def test_status_update_requires_login(self):
        response = self.client.get(
            reverse("statuses:update", kwargs={"pk": self.status.pk}))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('statuses:update', kwargs={'pk': self.status.pk})}",
        )

    def test_status_delete_requires_login(self):
        response = self.client.get(
            reverse("statuses:delete", kwargs={"pk": self.status.pk}))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('statuses:delete', kwargs={'pk': self.status.pk})}",
        )
