from django.shortcuts import render
from django.views import generic
from todo.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task
    template_name = "todo/task_list.html"
    queryset = Task.objects.prefetch_related("tags")
    paginate_by = 5


class TagListView(generic.ListView):
    model = Tag
    template_name = "todo/tag_list.html"
    paginate_by = 10
    queryset = Tag.objects.prefetch_related("tasks")
