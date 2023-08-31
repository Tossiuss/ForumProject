from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from .models import Comment, Rating


class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.name')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comments = Comment.objects.create(author=user, **validated_data)
        return comments

    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.name')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('ratings')
        instance.save()
        return super().update(instance, validated_data)
