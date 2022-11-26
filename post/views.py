from rest_framework.views import APIView
from rest_framework.response import Response
from post.models import Article, Post
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


class PostView(APIView):
    def get(self, request):
        articles = Post.objects.all()
        serializer = PostListSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            posts = serializer.save(user=request.user)
            serializer = PostCreateSerializer(posts)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# 22.11.23


class ArticleView(APIView):

    def get(self, request):
        articles = ArticleModel.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

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
            return Response(articles.data)
        else:
            return Response(articles.errors)


class ArticleDetailView(APIView):

    # if request.user.is_authenticated: 추후 JWT 변경 시 삭제.

    def get_object(self, pk):

        try:
            return ArticleModel.objects.get(pk=pk)

        except ArticleModel.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        articles = get_object_or_404(ArticleModel, pk=pk)
        serializer = ArticleSerializer(articles)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 수정 준비 중.
    def put(self, request, pk):
        articles = get_object_or_404(ArticleModel, pk=pk)
        serializer = ArticleSerializer(
            articles, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        articles = get_object_or_404(ArticleModel, pk=pk)
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


class LikeView(APIView):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("unfollow했습니다.", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("follow했습니다.", status=status.HTTP_200_OK)
        
        
# class LikeView(APIView):
#     def post(self, request, article_id):
#         user = request.user
#         article = ArticleModel.objects.get(id=article_id)
#         likes = article.like.all()
#         like_lists = []
#         for like in likes:
#             like_lists.append(like.id)
#         if user.id in like_lists:
#             article.like.remove(user)
            
#             article.like -= 1
#             article.save()
#             return Response({'message': '좋아요 취소!'})
#         else:
#             article.like.add(user)
            
#             article.like += 1
#             article.save()
#             return Response({'message': '좋아요!'})