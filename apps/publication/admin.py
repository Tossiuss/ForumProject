from django.contrib import admin
from .models import Teams, Tag, Posts
from apps.review.models import Comment, Like, Rating


class CommentInline(admin.TabularInline):
    model = Comment

class LikeInline(admin.TabularInline):
    model = Like

class RatingInline(admin.TabularInline):
    model = Rating


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, LikeInline, RatingInline]


admin.site.register(Teams)
admin.site.register(Tag)
admin.site.register(Posts, PostAdmin)
