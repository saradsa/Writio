from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import random

from .models import CustomUser, Category, Blog, Comment
from .utils import get_current_user, get_random_posts, get_category_number, get_popular_posts, get_all_categories, get_comments

# Create your views here.


def index(request):
	# All blogs displayed in descending publish date
	blogs = Blog.objects.all().order_by("-publish_date")

	return render(request, "blog/index.html", {
		"user": get_current_user(request),
		"categories": get_all_categories(),
		"blogs": blogs,
		"popblogs": get_popular_posts(),
		"randomblogs": get_random_posts(),
		"allposts": get_category_number()
		})


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def login_view(request):
	if request.method == "POST":
		User = get_user_model()

		# Sign in
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		# Check authentication
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('index'))
		else:
			return render(request, "blog/login.html", {
				"message": "Invalid username and/or password",
				"categories": get_all_categories()
				})
	else:
		return render(request, "blog/login.html", {
			"categories": get_all_categories()
			})

def register(request):
	if request.method == 'POST':
		User = get_user_model()
		username = request.POST['username']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		bio = request.POST['bio']
		if 'profile_picture' in request.FILES:
			profile_picture = request.FILES['profile_picture']
		else:
			profile_picture = None

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST['confirmation']

		if password != confirmation:
			return render(request, "blog/register.html", {
				"password_message": "Passwords must match",
				"categories": get_all_categories()
				})

		# Attempt to create a new user
		try:
			user = User.objects.create_user(email=email, username=username, first_name=first_name, last_name=last_name, password=password, bio=bio, profile_picture=profile_picture)
			user.save()
		except IntegrityError:
			return render(request, "blog/register.html", {
				"categories": get_all_categories(),
				"message": "Username already taken."
				})
		login(request, user)
		return HttpResponseRedirect(reverse('index'))
	else:
		return render(request, "blog/register.html", {
			"categories": get_all_categories()
			})

@login_required
def write(request):
	if request.method == "POST":
		title = request.POST['title']
		content = request.POST['content']
		category = request.POST['category']
		tags = request.POST['tags']

		if 'cover_image' in request.FILES:
			cover_image = request.FILES['cover_image']
		else:
			cover_image = None

		newBlog = Blog(
			title=title,
			content=content,
			cover_image = cover_image,
			author = get_current_user(request),
			category = Category(pk=category),
			tags = tags)

		newBlog.save()
		return HttpResponseRedirect(reverse("index"))

	return render(request, "blog/create.html", {
		"categories": get_all_categories()
		})



def single_blog(request, blog_id):

	if request.method == "POST":
		comment = request.POST['comment']

		newComment = Comment(
			post = Blog.objects.get(pk=blog_id),
			author = get_current_user(request),
			comment = comment
			)
		newComment.save()
		return HttpResponseRedirect(reverse("single_blog", kwargs={"blog_id": blog_id}))

	blog = Blog.objects.get(pk=blog_id)
	if get_current_user(request) != blog.author:
			blog.views += 1
	blog.save()
	blog = Blog.objects.get(pk=blog_id)
	comments = Comment.objects.filter(post=blog)
	
	comment_count = comments.count()
	
	return render(request, "blog/single_blog.html", {
		"blog": blog,
		"threeblogs": get_random_posts(),
		"categories": get_all_categories(),
		"allposts": get_category_number(),
		"comments": get_comments(blog_id),
		"comment_count": comment_count
		})






def category(request, category_name):
	category = category_name
	# Fetching all categories for the navbar
	categories = Category.objects.all()
	allposts = Blog.objects.filter(category__name=category_name)
	return render(request, "blog/category.html", {
		"blogs" : allposts,
		"category": category_name,
		"categories": get_all_categories(),
		"allposts": get_category_number(),
		"popblogs": get_popular_posts()
		})

