from django.db import models
from users.models import User

# Create your models here.


# class Post(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=50)
#     content = models.TextField()
#     image = models.ImageField(blank=True, upload_to='%Y/%m/')
#     created_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.title)


# 22.11.23


class Article(models.Model):

    ''' Article Definition'''

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,

    )
    picture = models.CharField(
        max_length=150,
    )

    title = models.CharField(
        verbose_name="게시글 제목",
        max_length=150,
    )
    content = models.TextField(
        verbose_name="게시글 내용",

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

    '''Categories Definition'''

    class CategoryChoice(models.TextChoices):
        EC_COMPOSITION = (
            "eccv16/composition_vii.t7",
            "EC_컴포지션"
        )
        EC_MUSE = (
            "eccv16/la_muse.t7",
            "EC_뮤즈"
        )
        EC_STARRY = (
            "eccv16/starry_night.t7",
            "EC_나이트"
        )
        EC_WAVE = (
            "eccv16/the_wave.t7",
            "EC_웨이브"
        )
        IN_CANDY = (
            "instance_norm/candy.t7",
            "IN_캔디"
        )
        IN_FEATHER = (
            "instance_norm/feathers.t7",
            "IN_패덜"
        )
        IN_MUSE = (
            "instance_norm/la_muse.t7",
            "IN_뮤즈"
        )
        IN_MOSAIC = (
            "instance_norm/mosaic.t7",
            "IN_모자이크"
        )
        IN_STARRY = (
            "instance_norm/starry_night.t7",
            "IN_나이트"
        )
        IN_UDNIE = (
            "instance_norm/udnie.t7",
            "IN_우드네"
        )

    category = models.CharField(
        "카테고리",
        max_length=150,
        choices=CategoryChoice.choices
    )

    def __str__(self) -> str:
        return self.category


class Picture(models.Model):

    ''' Picture Definition'''

    image_style = models.ForeignKey(
        "post.Category",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    picture = models.ImageField(
        "그림 이미지",
        upload_to='',

    )

    def __str__(self) -> str:
        return str(self.image_style)


class Comment(models.Model):

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name="작성 게시글",
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name="작성자",
    )
    content = models.CharField(
        max_length=300,
        verbose_name="댓글",
    )

    created_at = models.DateTimeField(
        auto_now_add=True

    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self) -> str:
        return f"게시글 {self.article} : 작성자 {self.user} : 댓글{self.content}"
