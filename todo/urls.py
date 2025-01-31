from django.urls import path

from todo.views import (
    TaskListView,
    TagListView
)


urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("", TagListView.as_view(), name="tag-list")
]


app_name = "todo"
