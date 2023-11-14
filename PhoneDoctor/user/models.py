from django.db import models

# Create your models here.

class User(models.Model):
    fist_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    password = models.TextField()

    def __str__(self):
        return '{} {}'.format(self.fist_name, self.last_name)