
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120,unique=True,blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    

class Article(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=300,
        unique=True,
        blank=True
    )

    excerpt = models.TextField(
        max_length=500,
        blank=True
    )

    content = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='articles', blank=True,null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="articles"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ArticleLike(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='likes')
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='article_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['article','user'],
            name='unique_article_like_per_user'
        )]
    def __str__(self):
        return f"{self.user.email} likes {self.article.title}"
    
    
class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f" Comment by {self.user.email}"
    
    