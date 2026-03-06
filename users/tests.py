from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            password="strong-password-123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            first_name="Other",
            last_name="User",
            password="other-password-123",
        )

    def test_user_create(self):
        response = self.client.post(
            reverse("users:create"),
            {
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "username": "ivan123",
                "password1": "super-password-123",
                "password2": "super-password-123",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="ivan123").exists())

    def test_user_update(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("users:update", kwargs={"pk": self.user.pk}),
            {
                "first_name": "Updated",
                "last_name": "User",
                "username": "updateduser",
            },
        )

        self.user.refresh_from_db()

        self.assertRedirects(response, reverse("users:index"))
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.username, "updateduser")

    def test_user_delete(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("users:delete", kwargs={"pk": self.user.pk}),
        )

        self.assertRedirects(response, reverse("users:index"))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_user_cannot_update_another_user(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("users:update", kwargs={"pk": self.other_user.pk}),
            {
                "first_name": "Hacked",
                "last_name": "User",
                "username": "hackeduser",
            },
        )

        self.other_user.refresh_from_db()

        self.assertRedirects(response, reverse("users:index"))
        self.assertNotEqual(self.other_user.first_name, "Hacked")

    def test_user_cannot_delete_another_user(self):
        self.client.login(username="testuser", password="strong-password-123")

        response = self.client.post(
            reverse("users:delete", kwargs={"pk": self.other_user.pk}),
        )

        self.assertRedirects(response, reverse("users:index"))
        self.assertTrue(User.objects.filter(pk=self.other_user.pk).exists())
