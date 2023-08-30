from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('posts', PostView, basename='posts'),
# router.register('categories', PostView, basename='categories'),
# router.register('tags', PostView, basename='tags/'),





urlpatterns = [
    path('categories/', CategoryView.as_view()),
    path('tags/', TagView.as_view()),
    path('', include(router.urls)),
]