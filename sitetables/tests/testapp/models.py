from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=20)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.title
