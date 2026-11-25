from django.shortcuts import get_object_or_404

# Create your views here.

from rest_framework import viewsets
from django.db import models
from .models import Article,Category,ArticleLike,Comment
from .serializers import ArticleSerializer,CategorySerializer,CommentSerializer
from .permissions import IsAuthorEditorOrAdmin,IsEditorOrAdminOrReadOnly,IsCommentOwnerOrEditorAdmin
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Count

class ArticleViewSet(viewsets.ModelViewSet):

    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorEditorOrAdmin]

    def get_queryset(self):
        user = self.request.user

        # Annotate like count for every article
        queryset = Article.objects.annotate(
            like_count=Count("likes"),
            comment_count=Count("comments")
        ).select_related(
            "author",
            "category"
        ).prefetch_related(
            "comments__user"
        )
        # Anonymous users: published articles only
        if not user.is_authenticated:
            return queryset.filter(
                status=Article.Status.PUBLISHED
            )

        # Editor and Admin: all articles
        if user.role in ["editor", "admin"]:
            return queryset

        # Author: published articles + own articles
        if user.role == "author":
            return queryset.filter(
                models.Q(status=Article.Status.PUBLISHED) |
                models.Q(author=user)
            ).distinct()

        # Reader: published articles only
        return queryset.filter(
            status=Article.Status.PUBLISHED
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.filter(is_active=True)
    serializer_class=CategorySerializer
    permission_classes=[IsEditorOrAdminOrReadOnly]
    


class ArticleLikeView(APIView):
    permission_classes =[IsAuthenticated]
    
    def post(self,request,pk):
        try:
            article = Article.objects.get(pk=pk,status=Article.Status.PUBLISHED)
        except Article.DoesNotExist:
            return Response(
                {'detail':"Article not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        like,created = ArticleLike.objects.get_or_create(article=article,user=request.user)
        if not created:
            return Response(
                {"detail":"You already liked this article"},
                status = status.HTTP_200_OK
            )
        return Response(
            {'detail':'Article liked successfully.'},
            status=status.HTTP_201_CREATED
        )
    def delete(self,request,pk):
        deleted,_ = ArticleLike.objects.filter(article_id=pk,user=request.user).delete()
        if not deleted:
            return Response(
                {"detail": "You have not liked this article."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"detail": "Like removed successfully."},
            status=status.HTTP_200_OK
        )
        
        
        

class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsCommentOwnerOrEditorAdmin
    ]

    def get_queryset(self):
        user = self.request.user

        queryset = Comment.objects.select_related(
            "user",
            "article"
        )

        if not user.is_authenticated:
            return queryset

        if user.role in ["editor", "admin"]:
            return queryset

        return queryset.filter(
            models.Q(user=user) |
            models.Q(article__status=Article.Status.PUBLISHED)
        ).distinct()

    def perform_create(self, serializer):

        article = get_object_or_404(
            Article,
            pk=self.kwargs["article_pk"],
            status=Article.Status.PUBLISHED
        )

        serializer.save(
            article=article,
            user=self.request.user
        )