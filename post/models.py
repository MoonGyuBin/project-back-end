from django.db import models
from users.models import User

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


# 22.11.23

class Article(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,

    )
    picture = models.CharField(
        max_length=150,
    )

    title = models.CharField(
        "게시글 제목",
        max_length=150,
    )
    content = models.TextField(
        "게시글 내용"

    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self) -> str:
        return f"{self.owner}님의 작품{self.title} 입니다."


class Category(models.Model):
    category = models.CharField(
        "카테고리",
        max_length=150,
    )

    def __str__(self) -> str:
        return self.category


class Picture(models.Model):

    image_style = models.ForeignKey(
        "post.Category",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    picture = models.ImageField(
        "그림 이미지",
        upload_to='%Y/%m/',

    )

    def __str__(self) -> str:
        return str(self.image_style)
