from django.db import models
from django.contrib.auth.models import AbstractUser


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(auto_now=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name="newspapers")
    redactors = models.ManyToManyField("Redactor", related_name="newspaper_redactors")

    def __str__(self):
        return f"{self.topic.name} {self.title} {self.published_date}"


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=False, default=0)
    newspapers = models.ManyToManyField(Newspaper, related_name="redactor_newspapers")

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("catalog:redactor-detail", kwargs={"pk": self.pk})
