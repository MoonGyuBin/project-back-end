from django.contrib import admin
from post.models import Post as PostModel
from post.models import Article as ArticleModel
from post.models import Picture as PictureModel
from post.models import Category as CategoryModel
# Register your models here.

admin.site.register(PostModel)


@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):

    list_display = (
        "owner",
        "title",
        "content",
        "created_at"
    )

    list_filter = (
        "owner",
        "created_at",
    )


@admin.register(PictureModel)
class PictureAdmin(admin.ModelAdmin):
    list_display = (
        "image_style",
    )


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "category",
    )
