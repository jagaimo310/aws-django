from django.db import models

# Create your models here.
class Prompt(models.Model):
    prompt = models.TextField(max_length=500)
    image_url = models.URLField(max_length=500)

