import random

from .models import Blog, CustomUser, Category, Comment


def get_current_user(request):
	currentUser = request.user

	return currentUser

def get_category_number():
	categories = Category.objects.all()
	totalpost = []

	for category in categories:
		post = Blog.objects.filter(category=category)
		number = len(post)
		totalpost.append(number)

	return zip(categories, totalpost)

def get_random_posts():
	allrandomblogs = Blog.objects.all()
	threerandomblogs = random.sample(list(allrandomblogs), 3)

	return threerandomblogs

def get_popular_posts():
	allpopblogs = Blog.objects.all().order_by("-views")
	popblogs = allpopblogs[:4]

	return popblogs

def get_all_categories():
	categories = Category.objects.all()
	return categories

def get_comments(blog_id):
	comments = Comment.objects.all().filter(post=blog_id).order_by("-comment_date")
	number_of_comments = len(comments)
	return comments
