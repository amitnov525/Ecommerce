from base64 import urlsafe_b64decode
from email import message
from django.shortcuts import render,redirect
from accounts.forms import RegistrationForm
from accounts.models import MyUser
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse

# Create your views here.
def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            user=MyUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            current_site=get_current_site(request)
            mail_subject="Please Activate Your Account"
            message=render_to_string('accounts/account_verification.html', {'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
                })
            to_email=email 
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form=RegistrationForm()
    context={
            'form':form
        }
    return render(request,'accounts/register.html',context)

def login_user(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You are logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Ivalid Credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request,'You are Logged Out')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=MyUser._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,MyUser.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True 
        user.save()
        messages.success(request,'Congratulations Registration Successfull.')
        return redirect('login')
    else:
        messages.error(request,'Invalid Activation Link')
        return redirect('register')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dasboard.html')

def forgot_password(request):
    if request.method=="POST":
        email=request.POST['email']
        if MyUser.objects.filter(email=email).exists():
            user=MyUser.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject="PLEASE RESET YOUR PASSWORD"
            message=render_to_string('accounts/reset_password_email.html',
            {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_email=email 
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password Reset Mail has been sent to your mail')
            return redirect('login')
        else:
            messages.error(request,'Email Does not exist')
            return redirect('forgot_password')
    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=MyUser._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,MyUser.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid 
        messages.success(request,'Please Reset Your Password')
        return redirect('reset_password')
    else:
        messages.error(request,'Eiether invlid link or link expired')
        return redirect('login')

def reset_password(request):
    if request.method=="POST":
        password=request.POST['password']
        password1=request.POST['confirm_password']
        if password==password1:
            uid=request.session['uid']
            user=MyUser.objects.get(id=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Changed Successfully |')
            return redirect('login')
        else:
            messages.error(request,'Password does not match')
            return redirect('reset_password')
    else:
        return render(request,'accounts/resetpassword.html')

@login_required(login_url='login')
def change_password(request):
    if request.method=="POST":
        password=request.POST['password']
        password1=request.POST['confirm_password']
        if password==password1:
            id=request.user.id
            user=MyUser.objects.get(id=id)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Changed Successfully.Please Login')
            return redirect('login')
        else:
            messages.error(request,'Password does not exist. Please Try Again.')
            return redirect('change_password')
    else:
        return render(request,'accounts/changepassword.html')




