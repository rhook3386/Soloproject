from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = 'Last Name must be at least 2 characters'
        
        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors

    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        if not check:
            errors['email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), bcrypt.hashpw(check[0].password.encode(), bcrypt.gensalt())):
                errors['email'] = "Email and password do not match."
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
            type = form['type']
        )
class GroupManager(models.Manager):
    def group_validator(self, postData):
        errors = {}

        if len(postData['org']) < 5:
            errors['org'] = "Org must include at least 5 characters."
        if len(postData['descript']) < 10:
            errors['descript'] = "Description must be at least 10 characters long."
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=55)
    type = models.CharField(max_length=40)

    objects = UserManager()

class Organization(models.Model):
    org_name = models.CharField(max_length=45)
    org_desc = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_org', on_delete=models.CASCADE)
    media = models.ImageField(upload_to='')
    videofile = models.FileField(upload_to='')
    def _str_(self):
        return self.media.name
    user_join = models.ManyToManyField(User, related_name='liked_posts')



    objects = GroupManager()

