from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.

class Video(models.Model):
    title = models.CharField(default="   ", max_length=255, null=True, blank=True)
    video = models.FileField(upload_to="video/")
    description = RichTextField(blank=True, null=True)
    represent = models.FileField(blank=True, null=True,upload_to="represent/")
    label = models.CharField(null=True, max_length=255)

class Famous(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return  self.name

    def get_absolute_url(self):
        return reverse('list-famous')


class UpForm(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    label_detected = models.CharField(null=True, blank=True, max_length=255)