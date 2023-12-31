
from django.db import models

class Property(models.Model):
    name = models.CharField(max_length=255)
    cost = models.CharField(max_length=50)
    type = models.CharField(max_length=100)
    area = models.CharField(max_length=50)
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    link = models.URLField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


