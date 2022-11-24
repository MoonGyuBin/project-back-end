from rest_framework import serializers
from post.models import Post, Article, Picture, Category, Comment


# 게시글리스트 보기 GET
class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):  # 유저-> 이메일
        return obj.user.email

    class Meta:
        model = Post
        fields = ('pk', 'title', 'image', 'update_at', 'user',)  # pk = id


# 게시글 작성 POST
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'image', 'content')


# 22.11.23

# 개별 조회

# class ArticleSerializer(serializers.ModelSerializer):
#     pass


# 사진
class PictureSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return obj.owner.username

    class Meta:
        model = Picture
        fields = "__all__"

# 카테고리


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

        # 조회


class ArticleSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    image_styles = PictureSerializer(read_only=True)

    def get_owner(self, obj):
        return obj.owner.email

    class Meta:
        model = Article
        fields = (
            "owner",
            "picture",
            "title",
            "content",
            "image_styles",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.user.email

    class Meta:
        model = Comment
        fields = (
            "pk",
            "article",
            "user",
            "author",
            "content",

        )
        read_only_fields = (
            "created_at",
            "updated_at",
        )
