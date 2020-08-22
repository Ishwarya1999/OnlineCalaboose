
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,authenticate

from django.forms.utils import ValidationError

from . import models


class PublicRegistrationForm(forms.ModelForm):
 
	email = forms.CharField(max_length=100, required=True)
	flat_no = forms.CharField(max_length=10,required=True)
	st_name = forms.CharField(max_length=50,required=True)
	area = forms.CharField(max_length=50,required=True)
	city = forms.CharField(max_length=50,required=True)
	state = forms.CharField(max_length=50,required=True)
	pincode = forms.IntegerField(required=True)
	phno = forms.IntegerField(required=True)
	

	#ModelForm does not have password field. SO we have defined it. 
	#UserCreationForm does not allow the commit argument, so it is not used. :p

	password1 = forms.CharField(label= 'Password', widget=forms.PasswordInput, required=True, min_length=8)
	password2 = forms.CharField(label= 'Confirm Password', widget=forms.PasswordInput, required=True, min_length=8)

	#to check for unique email constraint
	def clean_email(self):
		email = self.cleaned_data['email']
		User = get_user_model()
		qs = User.objects.filter(email = email)
		if qs.exists():
			raise forms.ValidationError("Email exists")
		return email


	#to validate whether both the passwords are the same
	def clean_password2(self):

		password11 = self.cleaned_data['password1']
		password22 = self.cleaned_data['password2']
		if (password11 and password22) and (password11!=password22):
			raise forms.ValidationError("Passwords don't match")
		return password22




    
    
	class Meta(forms.ModelForm):
		model = get_user_model() 
		fields = ['email', 'username','first_name','last_name','password1','password2', 'flat_no', 'st_name',
					'area', 'city', 'state','pincode','phno']


	#saving the form. Here we first save the user and then save the public
	def save(self):
		#print("hello")
		user= super().save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']

		user.set_password(self.cleaned_data['password1'])
		user.ispublic = True
		
		user.save()

		pub = models.Public.objects.create(user=user) #we assign the user to the pgr
		pub.email = self.cleaned_data['email']
		pub.flat_no = self.cleaned_data['flat_no']
		pub.st_name = self.cleaned_data['st_name']
		pub.area = self.cleaned_data['area']
		pub.city = self.cleaned_data['city']
		pub.state = self.cleaned_data['state']
		pub.phno = self.cleaned_data['phno']
		pub.pincode = self.cleaned_data['pincode']

		pub.save()

		return user

User=get_user_model()
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Invalid credentials!')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class CompliantRegistrationForm(forms.ModelForm):
#	fir_no = forms.IntegerField()
#	status = forms.CharField(max_length=100)
	CHOICE = (('criminal','Criminal'),('civil','Civil'))
	body = forms.CharField(widget=forms.Textarea)
	category = forms.ChoiceField(widget=forms.RadioSelect, choices = CHOICE)
#	complianee_name = forms.CharField()
#	complianee_addr = forms.CharField()
	#reg_datetime = forms.DateTimeField(auto_now_add = True)
	#documents = forms.FileField(upload_to='documents/')

	# def __init__(self,*args,**kwargs):
	# 	request = kwargs.pop('request')
	# 	self.user = request.user
	# 	super(CompliantRegistrationForm,self).__init__(*args,**kwargs)

	def save(self,request):
		p_user = models.Public.objects.get(user=request.user)
		comp = models.Compliant.objects.create(pub_user=p_user)
		#comp.pub_user=p_user
		comp.body = self.cleaned_data['body']
		comp.category = self.cleaned_data['category']
		#comp.complianee_name = self.cleaned_data['complianee_name']
		#comp.complianee_addr = self.cleaned_data['complianee_addr']
		comp.save()		
		return comp

	class Meta(forms.ModelForm):
		model = models.Compliant 
		fields = ['body', 'category']


class HomeForm(forms.ModelForm):
	body = forms.CharField(max_length=300)
	category = forms.CharField(max_length=30)

	class Meta(forms.ModelForm):
		model = models.Compliant 
		fields = ['body', 'category']

class MissingPersonRegistrationForm(forms.ModelForm):
	name = forms.CharField(max_length=30)
	location = forms.CharField(max_length=70)
	lastseen = forms.DateField(widget=forms.SelectDateWidget)
	identificationmark = forms.CharField(max_length=50)
#	image = forms.ImageField(required=True)

	def save(self,request):
		obj = models.MissingPerson.objects.create(name = self.cleaned_data['name'])
		#instance = MissingPerson(img=request.FILES['img'])
        #instance.save()
		obj.location = self.cleaned_data['location']
		obj.last_seen = self.cleaned_data['lastseen']
		obj.id_mark = self.cleaned_data['identificationmark']
		obj.img = request.FILES['img']
		print("image ",obj.img)
		obj.save()
		return obj

	class Meta(forms.ModelForm):
		model = models.MissingPerson
		fields = ['name','location','lastseen','identificationmark','img']