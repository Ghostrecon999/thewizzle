from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm, UserChangeForm\
, PasswordResetForm
from django.contrib.auth import get_user_model, authenticate,login
from .models import EmailVerification
from django.core.exceptions import ValidationError
from .models import UserProfile
from django.db.models  import Q
from .tokens import verification_token

UserModel = get_user_model()

class LoginAuthentication (AuthenticationForm):
    username=forms.CharField(
                                        label="",
                                       
            widget=forms.TextInput(
                    attrs={"autofocus": True,
                            "class":"em",
                            "placeholder":"Email or username"
                            }),
    )	
    password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                                    "class":"pw",
                                                    "placeholder":"password",
                                                    "id":"password",
                                                    }),
        )

class NewPasswordResetForm(PasswordResetForm):
    email=forms.CharField(
            label="",
            max_length=254,
            widget=forms.TextInput(attrs={"autocomplete": "email",
                                                    "class":"data",
                                                    "placeholder":"Email or username"
                                                    }),
    )
    def get_users(self, username_or_email):
        email_field_name=UserModel.get_email_field_name()
        users=UserModel.objects.filter(Q(username__iexact=username_or_email) | Q( email__iexact=username_or_email))
        return [u for u in users if u.is_active and u.has_usable_password() ]



class CustomUserCreation(UserCreationForm, PasswordResetForm):
    error_message={"exists":"This email is unavailable for use"}
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["email"].widget.attrs.update({"placeholder":"Email"})
        self.fields["password1"].widget.attrs.update({"placeholder":"Password","id":"password"})
        self.fields["password2"].widget.attrs.update({"placeholder":"Confirm password", "id":"password"})
        
    def clean_email(self):
        email=self.cleaned_data["email"]
        if UserModel.objects.filter(email=email).exists():
            raise ValidationError(self.error_message["exists"],code="exists")
        return email
            
            
    def save(self,*args,**kwargs):
        s=super().save(commit=False)
        s.is_active=False
        s.save()
        new_user_email = self.cleaned_data["email"]
        from_email=kwargs.get("from_email")
        html_email_template_name=kwargs.get("html_email_template_name")
        extra_email_context=kwargs.get("extra_email_context")
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="accounts/create_user_email.html",
        user=UserModel.objects.get(email=new_user_email)
        _instance = EmailVerification.objects.get_or_create(user=user)
        _message = _instance[0].verification_code
        context = {
                "email":new_user_email,
                "user":"new user",
                "code":_message,
                **(extra_email_context or {}),
            }
        self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                new_user_email,
                html_email_template_name=html_email_template_name,
            )
     
    class Meta:
        model = UserModel 
        fields = ("email",)

class CustomUserChange(UserChangeForm):
    class Meta:
        model=UserModel 
        fields="__all__"

class Verify(forms.Form):
    verify=forms.CharField(max_length=6, 
                                    label="Enter code",
                                    widget=forms.NumberInput(attrs={"autofocus":True}))
                                    
    

class CustomUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label="Username"
        self.fields["first_name"].label="Firstname"
        self.fields["last_name"].label="Lastname"
        
    
            
        
    class Meta:
        model=UserModel
        fields=["username","first_name","last_name",]

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_of_birth"].widget=forms.DateInput(attrs=
                                                                    {"type": "date",
                                                                      "min":"2009-01-01"
                                                                    },
                                                                    
                                                                    )
        
    class Meta:
        model=UserProfile
        fields=["date_of_birth","gender"]


class AddPhoto(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["photo",]