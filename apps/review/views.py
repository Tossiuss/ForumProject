from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import CommentSerializer
from apps.publication.permissions import *
from rest_framework.permissions import AllowAny

# Create your views here.

class PermissionsMixin:
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class CommentView(PermissionsMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
