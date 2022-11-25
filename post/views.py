from rest_framework.views import APIView
from rest_framework.response import Response
from post.models import Post
from post.serializers import PostListSerializer, PostCreateSerializer

# 22.11.23
from post.models import Article as ArticleModel
from post.models import Category as CategoryModel
from post.models import Picture as PictureModel
from post.models import Comment as CommentModel

from post.serializers import ArticleSerializer
from post.serializers import CommentSerializer

from post.transform import transform_img

from rest_framework.exceptions import NotAuthenticated
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from datetime import datetime

# Create your views here.


# class PostView(APIView):
#     def get(self, request):
#         articles = Post.objects.all()
#         serializer = PostListSerializer(articles, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             posts = serializer.save(user=request.user)
#             serializer = PostCreateSerializer(posts)
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# 22.11.23


class ArticleView(APIView):

    def get(self, request):
        articles = ArticleModel.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        fs = FileSystemStorage()
        datetimes = datetime.now().strftime('%Y-%m-%d %S')

        # if request.user.is_authenticated: 추후 JWT 변경 시 삭제.
        data = request.data
        categoies = CategoryModel.objects.get(
            category=request.data["image_style"])
        photo = request.FILES["picture"]

        pictures = fs.save(f"img{datetimes}.jpg", photo)
        transform = transform_img(categoies, pictures)

        picture = PictureModel.objects.create(
            image_style=categoies,
            picture=transform,
        )
        picture.save()

        data = {

            "owner": request.user.id,
            "picture": transform,
            "image_styles": categoies,
            "title": request.data["title"],
            "content": request.data["content"],
        }

        articles = ArticleSerializer(data=data)

        if articles.is_valid():
            articles.save(owner=request.user)
            return Response(articles.data, status=status.HTTP_201_CREATED)
        else:
            return Response(articles.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):

    # if request.user.is_authenticated: 추후 JWT 변경 시 삭제.

    def get_object(self, article_pk):

        try:
            return ArticleModel.objects.get(pk=article_pk)

        except ArticleModel.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, article_pk):
        articles = get_object_or_404(ArticleModel, pk=article_pk)
        serializer = ArticleSerializer(articles)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 수정 준비 중.
    def put(self, request, article_pk):
        articles = get_object_or_404(ArticleModel, pk=article_pk)
        serializer = ArticleSerializer(
            articles, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_pk):
        articles = get_object_or_404(ArticleModel, pk=article_pk)
        articles.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):

    def get(self, request):
        comments = CommentModel.objects.filter()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):

    def get(self, request, author_pk):
        comments = CommentModel.objects.filter(pk=author_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, author_pk):
        comments = get_object_or_404(CommentModel, pk=author_pk)
        serializer = CommentSerializer(
            comments, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delet(self, request, author_pk):
        comments = get_object_or_404(CommentModel, pk=author_pk)
        comments.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
