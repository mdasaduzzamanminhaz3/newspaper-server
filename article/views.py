from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from django.db import models
from .models import Article,Category
from .serializers import ArticleSerializer,CategorySerializer
from .permissions import IsAuthorEditorOrAdmin,IsEditorOrAdminOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):

    serializer_class = ArticleSerializer

    permission_classes = [
        IsAuthorEditorOrAdmin,
    ]

    def get_queryset(self):
        user = self.request.user

        # Public users can see published articles only
        if not user.is_authenticated:
            return Article.objects.filter(
                status=Article.Status.PUBLISHED
            )

        # Editor and Admin can see all articles
        if user.role in ["editor", "admin"]:
            return Article.objects.all()

        # Author can see own articles and published articles
        if user.role == "author":
            return Article.objects.filter(
                models.Q(status=Article.Status.PUBLISHED) |
                models.Q(author=user)
            ).distinct()

        # Reader can see published articles only
        return Article.objects.filter(
            status=Article.Status.PUBLISHED
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.filter(is_active=True)
    serializer_class=CategorySerializer
    permission_classes=[IsEditorOrAdminOrReadOnly]