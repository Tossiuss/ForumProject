from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import *
from apps.review.serializers import CommentSerializer
from django.db.models import Avg



class CategorySerializer(ModelSerializer):

    class Meta:
        model = Teams
        fields = ('title',)


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('title',)


class PostDetailSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.name')

    class Meta:
        model = Posts
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        tags = validated_data.pop('tags', [])
        post = Posts.objects.create(author=user, **validated_data)
        post.tags.add(*tags)
        return post


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return rep


class PostListSerialize(ModelSerializer):

    class Meta:
        model = Posts
        fields = ['author', 'title']
