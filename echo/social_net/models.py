from django.db import models
from accounts.models import CustomUser as User
from resources import CATEGORIES
from django.core.mail import send_mail


class Category(models.Model):
    categories = models.CharField(max_length=2, choices=CATEGORIES, default='MV')
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.categories


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='post_user')
    date_created = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=100)
    image1 = models.ImageField(null=True, blank=True)
    content = models.TextField()
    estimation = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def preview(self):
        return self.content[:100] + '...' if len(self.content) > 100 else self.content

    def __str__(self):
        return f'{self.header}: {self.content[:100]}'


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    comment = models.BooleanField(default=False)

    def send_email(self):
        subject = 'Отклик на публикацию'
        message = 'Здравствуйте! На вашу публикацию "{}" появился новый отклик. С уважением, Echo.'. \
            format(self.post.header)
        from_email = 'admin_email'
        recipient_list = [self.post.author.email]

        send_mail(subject, message, from_email, recipient_list)

    def __str__(self):
        return self.text


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
