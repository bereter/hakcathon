from django.db import models
from django.contrib.auth.models import User
from resources import *
from django.urls import reverse
from django.core.mail import send_mail
from django.db.models.functions import Coalesce
from django.db.models import Sum

# Create your models here.


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).\
            aggregate(p_r=Coalesce(Sum('post_rating'), 0))['p_r']

        self.rating = post_rating
        self.save()

    def __str__(self):
        return self.author.username



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, default=None)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    categories = models.CharField(max_length=2, choices=CATEGORIES, default='MV')
    header = models.CharField(max_length=100)
    content = models.TextField(null=True)
#    image = models.ImageField()
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f'{self.header}: {self.content[:100]}'

    def like(self):
        self.post_rating += 1
        self.save()

    def preview(self):
        return self.content[:100] + '...' if len(self.content) > 100 else self.content




class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    comment = models.BooleanField(default=False)

    def send_email(self):
        subject = 'Отклик на публикацию'
        message = 'Здравствуйте! На вашу публикацию "{}" появился новый отклик. С уважением, Echo.'.\
            format(self.post.header)
        from_email = 'admin_email'
        recipient_list = [self.post.author.email]

        send_mail(subject, message, from_email, recipient_list)

    def __str__(self):
        return self.text
