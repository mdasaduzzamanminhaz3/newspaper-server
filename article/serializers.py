
from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):

    author_email = serializers.EmailField(
        source="author.email",
        read_only=True
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "content",
            "author",
            "author_email",
            "status",
            "created_at",
            "updated_at",
            "published_at",
        ]

        read_only_fields = [
            "id",
            "slug",
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
