from django.urls import path
from . import views


urlpatterns = [
	path("", views.index, name="index"),
	path("login/", views.login_view, name="login"),
	path("logout/", views.logout_view, name="logout"),
	path("register/", views.register, name="register"),
	path("create/", views.write, name="write"),
	path("blog/<int:blog_id>/", views.single_blog, name="single_blog"),
	path("category/<str:category_name>/", views.category, name="category")
]