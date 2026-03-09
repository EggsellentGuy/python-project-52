from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="author",
            password="strong-password-123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="other-password-123",
        )
        self.status = Status.objects.create(name="Новый")
        self.label = Label.objects.create(name="Срочно")

        self.task = Task.objects.create(
            name="Подготовить отчет",
            description="Тестовое описание",
            status=self.status,
            author=self.author,
            executor=self.other_user,
        )
        self.task.labels.add(self.label)

    def test_task_list(self):
        self.client.login(username="author", password="strong-password-123")
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Подготовить отчет")

    def test_task_detail(self):
        self.client.login(username="author", password="strong-password-123")
        response = self.client.get(
            reverse("tasks:detail", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Подготовить отчет")
        self.assertContains(response, "Тестовое описание")

    def test_task_create(self):
        self.client.login(username="author", password="strong-password-123")

        response = self.client.post(
            reverse("tasks:create"),
            {
                "name": "Новая задача",
                "description": "Описание новой задачи",
                "status": self.status.pk,
                "executor": self.other_user.pk,
                "labels": [self.label.pk],
            },
        )

        self.assertRedirects(response, reverse("tasks:index"))
        self.assertTrue(Task.objects.filter(name="Новая задача").exists())

        task = Task.objects.get(name="Новая задача")
        self.assertEqual(task.author, self.author)
        self.assertEqual(task.executor, self.other_user)
        self.assertEqual(task.status, self.status)
        self.assertIn(self.label, task.labels.all())

    def test_task_update(self):
        self.client.login(username="author", password="strong-password-123")

        response = self.client.post(
            reverse("tasks:update", kwargs={"pk": self.task.pk}),
            {
                "name": "Обновленная задача",
                "description": "Новое описание",
                "status": self.status.pk,
                "executor": self.author.pk,
                "labels": [self.label.pk],
            },
        )

        self.task.refresh_from_db()

        self.assertRedirects(response, reverse("tasks:index"))
        self.assertEqual(self.task.name, "Обновленная задача")
        self.assertEqual(self.task.description, "Новое описание")
        self.assertEqual(self.task.executor, self.author)

    def test_task_delete_by_author(self):
        self.client.login(username="author", password="strong-password-123")

        response = self.client.post(
            reverse("tasks:delete", kwargs={"pk": self.task.pk}),
        )

        self.assertRedirects(response, reverse("tasks:index"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_non_author_forbidden(self):
        self.client.login(username="otheruser", password="other-password-123")

        response = self.client.post(
            reverse("tasks:delete", kwargs={"pk": self.task.pk}),
        )

        self.assertRedirects(response, reverse("tasks:index"))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_list_requires_login(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('tasks:index')}",
        )

    def test_task_create_requires_login(self):
        response = self.client.get(reverse("tasks:create"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('tasks:create')}",
        )

    def test_task_update_requires_login(self):
        response = self.client.get(
            reverse("tasks:update", kwargs={"pk": self.task.pk}))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('tasks:update', kwargs={'pk': self.task.pk})}",
        )

    def test_task_delete_requires_login(self):
        response = self.client.get(
            reverse("tasks:delete", kwargs={"pk": self.task.pk}))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('tasks:delete', kwargs={'pk': self.task.pk})}",
        )

    def test_task_detail_requires_login(self):
        response = self.client.get(
            reverse("tasks:detail", kwargs={"pk": self.task.pk}))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('tasks:detail', kwargs={'pk': self.task.pk})}",
        )
