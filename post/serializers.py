from rest_framework import serializers
from post.models import Article, Picture, Category, Comment

# 22.11.23


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
class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    
    def get_user(self,obj):
        return obj.user.email
    
    def get_like_count(self, obj):
        return obj.likes.count()
    class Meta:
        model = Article
        fields= ()




class ArticleSerializer(serializers.ModelSerializer):
    likes = serializers.StringRelatedField(many=True) # add likes serializers 
    
    likes_count = serializers.SerializerMethodField()
    
    owner = serializers.SerializerMethodField()
    image_styles = PictureSerializer(read_only=True)

    # def create(self, validated_data):
    #     validated_data.pop('like')
    
    def get_owner(self, obj):
        return obj.owner.email

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    class Meta:
        model = Article
        fields = (
            "id",
            "owner",
            "picture",
            "title",
            "content",
            "image_styles",
            "likes",
            "likes_count",
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
