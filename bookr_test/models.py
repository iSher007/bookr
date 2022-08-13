from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=50, help_text="Name of the Publisher")
    website = models.URLField(help_text="The website url of the Publisher")
    email = models.EmailField(help_text='Email of the Publisher')

    def __str__(self):
        return self.name
