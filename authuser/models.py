from django.db import models
from django.conf import settings
import uuid
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from microblog.models import*


# Create your models here.
class CustomUser(AbstractUser):
    email=models.EmailField(max_length=150,
                                unique=True
                                )
    username=models.CharField(max_length=30,
                                      help_text="maximum of 30 letters",
                                      null=True,
                                      unique=True,
                                      error_messages={"unique":"This username is unavailable for use"}
                                      )
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username"]
    
    def __str__(self):
        return self.username or self.email                                      
                                      
class UserProfile(models.Model):
    class Gender(models.TextChoices):
        Male='M','Male'
        Female='F','Female'
        Prefer_not_to_say="N","Prefer Not to say"

    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth=models.DateField(blank=True,null=True)
    gender=models.CharField(max_length=1,choices=Gender.choices, default=Gender.Prefer_not_to_say)
    biography=models.CharField(max_length=150,blank=True,null=True)
    photo = models.ImageField(upload_to='users_profile_pic/%Y/%m/%d/',blank=True,null=True)
    saved_posts=models.ManyToManyField(Post,related_name="saved",blank=True)
    favorites=models.ManyToManyField('self',symmetrical=False,blank=True, editable=False)
    following=models.ManyToManyField('self', through='Members',related_name='followers',symmetrical=False, blank=True, editable=False)

    
    def __str__(self):
        return self.user.email


class Members(models.Model):
    user1=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='user1_relates')
    user2=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='user2_relates')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['-created']),]     
        ordering = ['-created'] 

    def __str__(self):
        return f'{self.user1} follows {self.user2}'



def random_code():
    import random
    from string import digits
    secure_random = random.SystemRandom()
    return "".join(secure_random.choice(digits) for i in range(6))



class EmailVerification(models.Model):
    id=models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    verification_code=models.CharField(max_length=6,default=random_code)
    
    
    def get_absolute_url(self):
        return reverse('authuser:verify',args=[str(self.id),])
    
    