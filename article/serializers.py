
from rest_framework import serializers
from .models import Article,Category,ArticleLike,Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= ['id','name','slug','description','is_active','created_at']
        read_only_fields = ['id','slug','created_at']



class CommentSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "user_email",
            "content",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "user_email",
            "status",
            "created_at",
        ]

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Comment cannot be empty."
            )

        return value.strip()



class ArticleSerializer(serializers.ModelSerializer):

    author_email = serializers.EmailField(
        source="author.email",
        read_only=True
    )
    like_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "content",
            'category',
            "author",
            "author_email",
            "like_count",
            "comment_count",
            "comments",
            "status",
            "created_at",
            "updated_at",
            "published_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "like_count",
            "comments",
            "comment_count",
            "author",
            "author_email",
            "created_at",
            "updated_at",
            "published_at",
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Article title cannot be empty."
            )

        return value.strip()

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Article content cannot be empty."
            )

        return value.strip()


class ArticleLikeSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email",read_only=True)
    class Meta:
        model=ArticleLike
        fields=['id','article','user','user_email','created_at']
        read_only_fields=['id','user','user_email','created_at']
        
        
        

