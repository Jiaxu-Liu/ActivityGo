from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length = 50)
	phone = models.CharField(max_length=50)
	headImg = models.FileField(upload_to = 'activity/static/images/', default = 'activity/static/01.jpg')

	def __unicode__(self):
		return self.username

class Activities(models.Model):
	aname = models.CharField(max_length=50)
	adate = models.CharField(max_length=20)
	alocation = models.CharField(max_length=50)
	adescription = models.CharField(max_length=200)
	aorganiser = models.CharField(max_length=50)
	aparticipants = models.ManyToManyField('User')
	aparticipantnum = models.IntegerField(default=0)
	astatus = models.IntegerField(default=0)
	def __unicode__(self):
		return self.aname