from django.contrib.auth import models
# Create your models here.


class User(models.User, models.PermissionsMixin):
    def __str__(self):
        return self.username
