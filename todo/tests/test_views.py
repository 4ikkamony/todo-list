from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from todo.models import Task


class ToggleTaskStatusTest(TestCase):
    def setUp(self):
        self.task_done = Task.objects.create(
            content="Done Task",
            is_done=True,
        )
        self.task_not_done = Task.objects.create(
            content="Not Done Task",
            is_done=False,
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.post(f"/tasks/{self.task_done.pk}/toggle-status/")
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        response = self.client.post(
            reverse("todo:task-toggle-status", kwargs={"pk": self.task_done.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_toggle_done_task(self):
        response = self.client.post(
            reverse("todo:task-toggle-status", kwargs={"pk": self.task_done.pk})
        )
        self.assertRedirects(response, reverse("todo:task-list"))

        self.task_done.refresh_from_db()

        self.assertFalse(self.task_done.is_done)

    def test_toggle_not_done_task(self):
        response = self.client.post(
            reverse("todo:task-toggle-status", kwargs={"pk": self.task_not_done.pk})
        )
        self.assertRedirects(response, reverse("todo:task-list"))

        self.task_done.refresh_from_db()

        self.assertTrue(self.task_done.is_done)

    def test_toggle_task_that_not_exists(self):
        response = self.client.post(
            reverse("todo:task-toggle-status", kwargs={"pk": 9999})
        )
        self.assertEqual(response.status_code, 404)


class TaskListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_tasks = 8

        for task_id in range(number_of_tasks):
            Task.objects.create(
                content=f"{task_id} Task for testing purposes",
                is_done=True if task_id % 2 == 0 else False,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("todo:task-list"))
        self.assertEqual(response.status_code, 200)

    def test_must_be_ordered_by_is_done_asc_and_created_at_desc(self):
        response = self.client.get(reverse("todo:task-list"))

        task_context = response.context["task_list"]
        task_list = Task.objects.all().order_by("is_done", "-created_at")

        self.assertEqual(
            list(task_context),
            list(task_list[: len(task_context)]),
        )

    def test_must_be_paginated(self):
        response = self.client.get(reverse("todo:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)


class TaskCreateViewTest(TestCase):
    def test_create_task(self):
        response = self.client.post(
            reverse(
                "todo:task-create",
            ),
            {"content": "Test task"},
        )
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(id=1)
        self.assertEqual(task.content, "Test task")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/tasks/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("todo:task-create"))
        self.assertEqual(response.status_code, 200)


class TaskUpdateViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            content="Intitial task content",
            deadline=timezone.now() + timezone.timedelta(days=1)
        )
        self.initial_deadline = self.task.deadline

    def test_update_task_valid_data(self):
        response = self.client.post(
            reverse(
                "todo:task-update",
                kwargs={"pk": self.task.id}
            ),
            {"content": "New task content"},
        )

        Task.objects.get(id=self.task.id).refresh_from_db()

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Task.objects.get(id=self.task.id).content, "New task content"
        )

    def test_update_task_invalid_deadline(self):
        response = self.client.post(
            reverse(
                "todo:task-update",
                kwargs={"pk": self.task.id}
            ),
            {
                "content": "New task content",
                "deadline": self.initial_deadline - timezone.timedelta(days=5)
            },
        )

        self.assertEqual(response.status_code, 200)

        Task.objects.get(id=self.task.id).refresh_from_db()

        self.assertEqual(
            Task.objects.get(id=self.task.id).deadline,
            self.initial_deadline
        )


class TaskDeleteViewTest(TestCase):
    def test_delete_task(self):
        task = Task.objects.create(
            content="Intitial task content",
        )

        response = self.client.post(
            reverse(
                "todo:task-delete",
                kwargs={"pk": task.id},
            ),
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Task.objects.filter(id=task.id).exists()
        )
