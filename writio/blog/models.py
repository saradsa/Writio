from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
	profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
	bio = models.CharField(max_length=100, blank=True)
	


class Category(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class Blog(models.Model):
	title = models.CharField(max_length=60)
	content = models.TextField(default="")
	snippet = models.TextField(max_length=200, default="")
	cover_image = models.ImageField(upload_to='cover_photos', blank=True)
	author = models.ForeignKey(
		CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="user")
	category = models.ForeignKey(
		Category, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
	publish_date = models.DateTimeField(auto_now_add=True)
	tags = models.CharField(max_length=60, blank=True)
	views = models.PositiveIntegerField(default=0)


	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True, related_name="comment_on")
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="commented_by")
	comment = models.CharField(max_length=100, blank=True)
	comment_date = models.DateTimeField(auto_now_add=True)

