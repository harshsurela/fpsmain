from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class adminuser(models.Model):
    user = models.OneToOneField(User,default=False ,on_delete=models.CASCADE,primary_key=True)
    image = models.ImageField(upload_to="profilepics")
    image2 = models.ImageField(upload_to="profilepics")
    allowedUsage = models.IntegerField(default=1)
    blocked = models.BooleanField(default=False)
    email= models.CharField(max_length=200,default="")
    mobile= models.IntegerField(default=1)

    def __str__(self):
        return self.user.username

class subadminuser(models.Model):
    user = models.OneToOneField(User,default=False ,on_delete=models.CASCADE,primary_key=True)
    blocked = models.BooleanField(default=False)
    email= models.CharField(max_length=200,default="")
    mobile= models.IntegerField(default=1)
    admin = models.ForeignKey(adminuser,default=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class userprofile(models.Model):
    consent = models.BooleanField(default=False)
    username = models.CharField(max_length=60)
    father_name = models.CharField(max_length=60)
    mother_name = models.CharField(max_length=60)
    DOB = models.DateField( blank=True, null=True)
    address = models.CharField(max_length=300)
    contactno = models.IntegerField(default=1)
    email = models.CharField(max_length=50)
    school = models.CharField(max_length=150)
    # subadmin = models.ForeignKey(subadminuser,null=True,on_delete=models.CASCADE)
    datajoined = models.DateField(default=datetime.date.today)
    standard = models.CharField(max_length=100)
    bloodGroup = models.CharField(max_length=10)
    remarks=models.CharField(max_length=100,default="")
    # def save(self, *args, **kwargs):
    #     if self.subadmin is None:  # Set default reference
    #         self.subadmin = subadminuser.objects.get(admin=self.admin)
    #     super(userprofile, self).save(*args, **kwargs)

    def __str__(self):
        return self.username



class notify(models.Model):
    title = models.CharField(max_length=200,null=True)
    publishedDate = models.DateField(auto_now_add=True)
    greetdate = models.DateField()
    user = models.ForeignKey(userprofile,on_delete=models.CASCADE)
    admin = models.ForeignKey(adminuser,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.title



class adminnotify(models.Model):
    title = models.CharField(max_length=200,null=True)
    publishedDate = models.DateField(auto_now_add=True)
    greetdate = models.DateField()
    user = models.ForeignKey(adminuser,null=False,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class AccessToken(models.Model):
    token = models.CharField(max_length=100)
    is_used=models.BooleanField(default=False)
    def __str__(self):
        return self.token