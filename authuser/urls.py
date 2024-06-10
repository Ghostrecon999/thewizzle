from django.urls import path,include
from .views import verify,createuser, createprofile, addphoto
from django.contrib.auth import views
from django.urls import reverse_lazy
from .forms import LoginAuthentication, NewPasswordResetForm

app_name='authuser'
    
urlpatterns = [
    path('signup/',createuser,name='createuser'),
    
    path('verify/<id>/',verify, name='verify'),
    
     path('verify/<id>/<token>/',verify, name='verify'),
     
    path("createprofile/", createprofile, name="createprofile"),
    
    path("addphoto/", addphoto , name="addphoto"),
    
    path('login/', views.LoginView.as_view(form_class=LoginAuthentication,
                                           template_name = 'accounts/login.html'),\
                                           name='login'),
    
    path('logout/', views.LogoutView.as_view(template_name = 'accounts/logged_out.html'),\
                                             name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(success_url=reverse_lazy('authuser:password_change_done'),\
                                                              template_name = 'accounts/password_change_form.html'),\
                                                              name='password_change'),
    
    path('password_change/done/', views.PasswordChangeDoneView.as_view(template_name = 'accounts/password_change_done.html'),\
                                                                       name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(form_class=NewPasswordResetForm,
                                                            success_url=reverse_lazy('authuser:password_reset_done'),\
                                                            template_name = 'accounts/password_reset_form.html',\
                                                            email_template_name = 'accounts/password_reset_email.html'),\
                                                            name='password_reset'),
    
    path('password_reset/done/', views.PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_done.html'),\
                                                                    name='password_reset_done'),
        
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('authuser:password_reset_complete'),\
                                                                           template_name = 'accounts/password_reset_confirm.html'),\
                                                                           name='password_reset_confirm'),
    
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset_complete.html'),\
                                                                name='password_reset_complete'),
    
]