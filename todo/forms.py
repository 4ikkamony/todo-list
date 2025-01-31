from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from todo.models import Task, Tag


class TaskForm(forms.ModelForm):
    content = forms.CharField(
        label="Task Description",
        widget=forms.Textarea(
            attrs={"placeholder": "Describe the task..."}
        )

    )
    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control"
                }
        ),
    )
    tags = forms.ModelMultipleChoiceField(
        label="Add tags",
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-select tags-field"}
        ),
    )

    class Meta:
        model = Task
        fields = ("content", "deadline", "tags", )

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline:
            if deadline < timezone.now():
                raise ValidationError(
                    "The deadline cannot be in the past."
                )
        return deadline


class TagForm(forms.ModelForm):
    name = forms.CharField(
        label="Tag name",
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Enter tag name"})
    )
    class Meta:
        model = Tag
        fields = ("name", )
