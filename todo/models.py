from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="tasks")

    class Meta:
        ordering = (
            "is_done",
            "-created_at",
        )

    def __str__(self) -> str:
        status = "Done" if self.is_done else "Not Done"
        content_peek = self.content if len(self.content) <= 16 else self.content[:16]
        return f"{self.created_at} {status} {content_peek}..."
