from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from multiselectfield import MultiSelectField

class YourModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()

class Another(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2300)
    files = models.JSONField(
       models.ImageField()  
   )

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        print("user: ", user)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('plan', 'premium')

        return self.create_user(email, password, **extra_fields)



MY_CHOICES = ((1, 'pleb'),
               (2, 'premium'))

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    plan = MultiSelectField(choices=MY_CHOICES, max_choices=1, max_length=1)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    
class Category(models.Model):
    categorie = models.CharField(max_length=400)


    
class Meditation(models.Model):
    title = models.TextField()
    category = models.TextField()
    # tags = models.JSONField(models.TextField())
    # tags = models.JSONField()
    # tags = ArrayField(models.TextField())
    tags =  models.TextField()
    background = models.TextField()
    mp3 = models.TextField()
    voice = models.TextField()
    duration = models.IntegerField()
    premium = models.BooleanField()
    large = models.BooleanField()
    createdAt = models.TextField()
    plays = models.IntegerField()

class Breath(models.Model):
    name = models.TextField()
    mp3 = models.TextField()
    tempo = models.TextField()
    premium = models.BooleanField()
    createdAt = models.TextField()
    plays = models.IntegerField()
    
class Card(models.Model):
    excerpt = models.TextField()
    message = models.TextField()
    background = models.TextField()
    mp3 = models.TextField()
    createdAt = models.TextField()
    plays = models.IntegerField()    

class Sound(models.Model):
    title = models.TextField()
    category = models.TextField()
    thumbnail = models.TextField()
    background = models.TextField()
    mp3 = models.TextField()
    premium = models.BooleanField()
    createdAt = models.TextField()
    plays = models.IntegerField()    


class Yoga(models.Model):
    title = models.TextField()
    mp4 = models.TextField()
    duration = models.IntegerField()
    premium = models.BooleanField()
    createdAt = models.TextField()
    plays = models.IntegerField() 
    background = models.TextField()
       


class Podcast(models.Model):
    title = models.TextField()
    mp4 = models.TextField()
    duration = models.IntegerField()
    premium = models.BooleanField()
    createdAt = models.TextField()
    plays = models.IntegerField()    
    background = models.TextField()
