from django.contrib import admin
from .models import CustomUser, Category, Blog, Comment
from django.utils.html import format_html
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display = ['username', 'first_name', 'last_name', 'get_profile_picture']

	def get_profile_picture(self, obj):
		if obj.profile_picture:
			return format_html('<img src="{}" style="width: 200px; height: 150px;"/>'.format(obj.profile_picture.url))
		else:
			return 'No Image Found'

	get_profile_picture.allow_tags = True
	get_profile_picture.short_description = 'Profile Picture'


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name']


class BlogAdmin(admin.ModelAdmin):
	list_display = ['title', 'content', 'author', 'category', 'publish_date', 'get_cover_image']

	def get_cover_image(self, obj):
		if obj.cover_image:
			return format_html('<img src="{}" style="width: 200px; height:150px;"/>'.format(obj.cover_image.url))
		else:
			return 'No Image Found'

class CommentAdmin(admin.ModelAdmin):
	list_display = ['post', 'author', 'comment', 'comment_date']

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
