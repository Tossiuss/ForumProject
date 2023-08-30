from rest_framework.response import Response
from rest_framework import viewsets, filters, generics
from .serializers import *
import django_filters
from rest_framework.permissions import AllowAny
from .permissions import IsAuthorPermission, IsAdminPermission
from apps.review.serializers import *
from apps.review.models import *
from rest_framework.decorators import action

# Create your views here.

class CategoryView(generics.ListCreateAPIView):
    queryset = Teams.objects.all()
    serializer_class = CategorySerializer

class TagView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostView(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tags__slug', 'category', 'author']
    search_fields = ['title', 'body']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerialize
        return PostDetailSerializer

    @action(methods=['POST', 'PATCH'], detail=True)
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['post'] = pk
        serializer = RatingSerializer(data=data, context={'request': request})
        rating = Rating.objects.filter(author=request.user, post=pk).first()
        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response(
                    'Rating objact exists', status=200
                )
            elif rating and request.method == 'PATCH':
                serializer.update(rating, serializer.validated_data)
                return Response(
                    'ok', status=200
                )
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(
                    data='ok', status=201
                )


    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.delete()
            message = 'unlike'
            status = 204
        except Like.DoesNotExist:
            Like.objects.create(post=post, author=user)
            message = 'Liked'
            status = 201
        return Response(message, status=status)



    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()