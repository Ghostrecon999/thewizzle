from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreation,Verify, CustomUserForm, UserProfileForm
from .models import EmailVerification
from .models import UserProfile
from django.contrib.auth import get_user_model,login
from django.contrib import messages
from .tokens import verification_token


User=get_user_model()
    

# Create your views here.



def createuser(request):
    if request.method.lower()=='post':
        form=CustomUserCreation(request.POST)
        if form.is_valid():
            data={
                    "from_email":"emmanuelorende009@gmail.com",
                    "html_email_template_name":None,
                    "domain_override":None,
                    "request": request,
                    "extra_email_context":None,
            }
            new_user = form.save(**data)
            user=User.objects.get(email=form.cleaned_data["email"])
            _instance = EmailVerification.objects.get(user=user)
            token=verification_token.make_token(_instance)
            return redirect(_instance.get_absolute_url() + token) #redirect to verify email
            
    else:
        form=CustomUserCreation()
    return render(request,'accounts/signup.html',{'form':form})




def verify(request,id,token=None):
    form=Verify()
    _instance=get_object_or_404(EmailVerification, id=id)
    if verification_token.check_token(_instance, token):
        _message = _instance.verification_code
        if request.method.lower() == 'post':
            form=Verify(request.POST)
            if form.is_valid():
                if form.cleaned_data['verify'] == _message:            
                    _instance.user.is_active=True
                    _instance.user.save()
                    profile= UserProfile.objects.get_or_create(user=_instance.user)
                    login(request,_instance.user, backend="django.contrib.auth.backends.ModelBackend")
                    return redirect("authuser:createprofile")
            else:
                messages.error(request, 'Code invalid')
        return render(request,'accounts/verify.html',{'form':form})
    else:
        return render(request,"accounts/expired.html",{})
        


def createprofile(request):
    if request.method=="POST":
        user_form=CustomUserForm(instance=request.user,
                                        data=request.POST)
        profile_form=UserProfileForm(instance=request.user.userprofile,
                                data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect ("authuser:addphoto")
    else:
        user_form = CustomUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request,'accounts/signup2.html',
                            {'user_form': user_form,
                            'profile_form': profile_form})

def addphoto (request):
    if request.method=="POST":
        form=AddPhoto(instance=request.user,
                            files=request.FILES)
        if form.is_valid():
            form.save()
    else:
        form=AddPhoto (instance=request.user)
    return render(request,"accounts/addphoto.html",
                        {"form":form})
        
    