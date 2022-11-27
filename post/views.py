from rest_framework.views import APIView
from rest_framework.response import Response

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

# 22.11.23


# 게시글 조회 / 삭제
class ArticleView(APIView):

    def get(self, request):
        articles = ArticleModel.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        fs = FileSystemStorage()
        datetimes = datetime.now().strftime('%Y-%m-%d %S')

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


# 게시글 수정
class ArticleDetailView(APIView):

    def get_object(self, article_pk):

        try:
            return ArticleModel.objects.get(pk=article_pk)

        except ArticleModel.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, article_pk):
        articles = get_object_or_404(ArticleModel, pk=article_pk)
        serializer = ArticleSerializer(articles)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

# 댓글 조회 / 작성


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

# 댓글 조회 / 수정 / 삭제


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
