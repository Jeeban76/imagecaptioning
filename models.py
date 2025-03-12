from django.db import models

class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    caption = models.TextField(blank=True)

    def __str__(self):
        return self.caption