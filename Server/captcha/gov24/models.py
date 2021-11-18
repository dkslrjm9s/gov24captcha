from django.db import models


class AnaResults(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=6)
    time = models.TextField()
    img = models.ImageField(upload_to="data/")

    class Meta:
        ordering = ['created']

