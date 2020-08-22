from django.shortcuts import render
from .models import Public,Compliant,Police,Criminal,UnidentifiedBodies
from .forms import PublicRegistrationForm,UserLoginForm,CompliantRegistrationForm,MissingPersonRegistrationForm
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,get_user_model
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView,TemplateView
from django.core.mail import send_mail

# Create your views here.
def homepage(request):
	if request.method == 'POST':
		body = request.POST.get('body')
		mail = request.POST.get('mail')
		send_mail('Another Query',body,mail,['calaboose@gmail.com'])
	
	return render(request,'public/index.html')
	

def newPublic(request):
	if request.method=='POST':
		form = PublicRegistrationForm(request.POST,request.FILES) #instantiate the form

		if form.is_valid():

			pub_form = form.save() #save all the details
			pub_form.save() #save a pgr instance to the db
			print("SIGNUP SUCCESSFUL")
			return redirect('/')


		else:
			#if any of the details in the form is invalid we render the form again
			print(form.errors)
			return render(request,'public/publicSignup.html', {'form':form}) 




		
	#if the url is called with a GET method we simply return the form	
	else:
		print("GET method")
		form = PublicRegistrationForm()
		return render(request,'public/publicSignup.html', {'form':form})

def user_login(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user = authenticate(username=username, password=password)

        login(request, user)

        if request.user.ispublic == True:
            #return render(request,"public/publicmenu.html",{'firstname':request.user.first_name, 'lastname':request.user.last_name})
            return redirect('/public/login/publicmenu/')
        elif request.user.isforensic == True:
            print("Forensic Login")
            return render(request,"public/forensic.html",{'username':username})
        else:
        	return redirect('/public/login/police/')
           
        


    context = {
        'form': form,
    }
    return render(request, "public/login.html", context)


def user_logout(request):
    logout(request)
    return redirect('/')

def newCompliant(request):
	if request.method == 'POST':
		form = CompliantRegistrationForm(request.POST)
		if form.is_valid():
			print("Form valid")
			c_form = form.save(request)
			c_form.save()
			p_user = Public.objects.get(user=request.user)
			comp = Compliant.objects.get(pub_user=p_user,id=c_form.id)
			comp.complainee_name = request.POST.get('c_name')
			comp.complainee_addr = request.POST.get('c_addr')
			comp.pol_officer = Police.objects.get(area = comp.pub_user.area.lower())
			comp.save()
			return redirect('/public/login/publicmenu/')
		else:
			print("invalid")
			return render(request,"public/register_compliant.html",{'form':form})	

	else:
		print("GET method")
		form = CompliantRegistrationForm()
		return render(request,"public/register_compliant.html",{'form':form})	


def caseDisplay(request):
	posts = Compliant.objects.all()
	posts= posts.filter(pol_officer = Police.objects.get(user = request.user))
	args={'posts':posts,'username':request.user.username}
	return render(request,"public/cases.html",args)


def caseDetails(request,postid):
	if request.method=='GET':
		posts = Compliant.objects.all()
	#	case_id =  request.GET.get('caseid')
		print("caseid",postid)
		post= Compliant.objects.get(id = postid)
		args={'post':post}
		return render(request,'public/casedetails.html',args)
	elif request.method == 'POST':
		print("hello")
		newstatus = request.POST.get('status')
		post= Compliant.objects.get(id = postid)
		post.status = newstatus
		args = {'post':post}
		post.save()
		return render(request,'public/casedetails.html',args)
	else:
		return render(request,'public/cases.html')

def viewCompliant(request):
	posts = Compliant.objects.all()
	posts = posts.filter(pub_user= Public.objects.get(user = request.user))
	args = {'posts':posts,'username':request.user.username}
	return render(request,"public/viewcompliants.html",args)

def viewComplaintDetails(request,postid):
	if request.method=='GET':
		posts = Compliant.objects.all()
	#	case_id =  request.GET.get('caseid')
		print("caseid",postid)
		post= Compliant.objects.get(id = postid)
		args={'post':post}
		return render(request,'public/viewcompliantdetails.html',args)
	else:
		return render(request,'public/cases.html')

def viewCriminals(request):
	if request.method == 'GET':
		criminals = Criminal.objects.all()
		return render(request,'public/viewcriminal.html',{'criminals':criminals})
	else:
		return render(request,'public/publicmenu.html')

def viewUnidentBodies(request):
	if request.method == 'GET':
		posts = UnidentifiedBodies.objects.all()
		return render(request,'public/viewunidentifiedbodies.html',{'posts':posts})
	else:
		return render(request,'public/publicmenu.html')

def publicmenu(request):
	return render(request,"public/publicmenu.html",{'firstname':request.user.first_name, 'lastname':request.user.last_name})

def newMissingPerson(request):
	if request.method == 'POST':
		form = MissingPersonRegistrationForm(request.POST)
		if form.is_valid():
			obj = form.save(request)
			obj.save()
			return render(request,'public/missingpersonmsg.html')
		else:
			return render(request,'public/register_missingperson.html',{'form':form})
	else:
		form = MissingPersonRegistrationForm()
		return render(request,'public/register_missingperson.html',{'form':form})



def deletecase(request,id,postid):
	post=Compliant.objects.all()

	post=Compliant.objects.get(id = id)
	print("id",id)
	args={'post':post}
	#if request.method=='POST':
	print("hhhhhh")
	post.delete()
	return redirect(request,'../../')
	context={
		"object":post
	}
	#return render(request,"public/cases.html",context)

def delete(request,postid,id=None):
	instance=Compliant.objects.get(id=id)
	instance.delete()
	return render(request,"public/deletemsg.html")

def contact(request):
	return redirect('public/contact/')
		
