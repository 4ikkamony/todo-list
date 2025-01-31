from django.utils import timezone
from django.test import TestCase


from todo.forms import TaskForm


class TaskFormTest(TestCase):
    def test_clean_deadline_valid(self):
        future_deadline = timezone.now() + timezone.timedelta(days=1)
        form_data = {"content": "Test task", "deadline": future_deadline}
        form = TaskForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_clean_deadline_past(self):
        past_deadline = timezone.now() - timezone.timedelta(days=1)
        form_data = {"content": "Test task", "deadline": past_deadline}
        form = TaskForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_clean_deadline_not_specified(self):
        form_data = {"content": "Test task"}
        form = TaskForm(data=form_data)

        self.assertTrue(form.is_valid())
