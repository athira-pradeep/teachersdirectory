from django.db import models

# Create your models here.

class LoginTable(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class TeachersTable(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profilepic/',blank=True,null=True,default='profilepic/default.JPG')
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    roomno = models.CharField(max_length=100)
    subjects = models.CharField(max_length=500)

    def __str__(self):
        return self.firstname