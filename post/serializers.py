from rest_framework import serializers
from post.models import Post, Article, Picture, Category


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
        fields = (
            "owner",
            "image_style",
            "picture",
        )

# 카테고리


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

        # 조회


class ArticleSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(

    )
    picture = PictureSerializer(
        many=True,
        read_only=True,
        source="picture_set",
    )
    category = CategoriesSerializer(
        many=True,
        read_only=True,
        source="category_set",
    )

    def get_owner(self, obj):
        return obj.owner.email

    class Meta:
        model = Article
        fields = "__all__"
