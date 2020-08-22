from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from multiselectfield import MultiSelectField

# Create your models here.

#basic user details for login - same for public,police,forensic doctor and admin
class User(AbstractUser):
	ispublic = models.BooleanField(default = False)
	isforensic = models.BooleanField(default = False)
	ispolice = models.BooleanField(default = True)
		
class Public(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	email = models.CharField(max_length=100)
	flat_no = models.CharField(max_length=10)
	st_name = models.CharField(max_length=50)
	area = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	pincode = models.IntegerField(default=0)
	phno = models.IntegerField(default=0)

class Police(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	area = models.CharField(max_length=20)

class Compliant(models.Model):
	pub_user = models.ForeignKey(Public,on_delete=models.CASCADE)
	pol_officer = models.ForeignKey(Police,on_delete=models.CASCADE,null=True)
	complainee_name = models.CharField(max_length=30,default="No name")
	complainee_addr = models.CharField(max_length=250,default="No name")
	fir_no = models.IntegerField(default=0)
	status = models.CharField(max_length=100,default="No status")
	body = models.CharField(max_length=300)
	CHOICE = (('criminal','Criminal'),('civil','Civil'))
	category = MultiSelectField(choices=CHOICE)
	reg_datetime = models.DateField(auto_now_add = True)
	documents = models.FileField(upload_to='documents/')

class Criminal(models.Model):
	name = models.CharField(max_length=30)
	case_category = models.CharField(max_length=40)
	id_mark = models.CharField(max_length=50)
	img = models.ImageField(upload_to='criminal_imgs/',blank=True)

class UnidentifiedBodies(models.Model):
	id_mark = models.CharField(max_length=50)
	location = models.CharField(max_length=40)
	reason = models.CharField(max_length=70)
	date_of_death = models.DateField(auto_now_add=False)
	img = models.ImageField(upload_to='unidentBodies_imgs/',blank=True)

class MissingPerson(models.Model):
	name = models.CharField(max_length=30)
	location = models.CharField(max_length=70)
	last_seen = models.DateField(auto_now_add=False,null=True)
	id_mark = models.CharField(max_length=50)
	img = models.ImageField(upload_to='missing_imgs/',blank=True)



