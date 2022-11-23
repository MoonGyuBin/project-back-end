from rest_framework.views import APIView
from rest_framework.response import Response
from post.models import Post
from post.serializers import PostListSerializer, PostCreateSerializer

# 22.11.23
from rest_framework.exceptions import NotAuthenticated
from post.models import Article, Category, Picture
from .serializers import ArticleSerializer, CategoriesSerializer, PictureSerializer
from .transform import transform_img
from django.core.files.storage import FileSystemStorage
from datetime import datetime

# Create your views here.

# 게시글 리스트 보기/작성


class PostView(APIView):
    def get(self, request):
        articles = Post.objects.all()
        serializer = PostListSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            posts = serializer.save(user=request.user)
            print(posts)
            serializer = PostCreateSerializer(posts)
            print(serializer)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ArticleView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        categoies = Category.objects.get(
            category=request.data["image_style"])
        print(categoies)
        if request.FILES["picture"]:
            photo = request.FILES["picture"]
            fs = FileSystemStorage()
            datetimes = datetime.now().strftime('%Y-%m-%d %S')
            pictures = fs.save(f"img{datetimes}.jpg", photo)
            pass

        # # 모델이름 # 인풋 사진
        transform = transform_img(categoies, pictures)
        print(transform)

    # def post(self, request):
    #     if request.user.is_authenticated:
    #         serializer = ArticleSerializer(data=request.data)
    #         print(serializer)
    #         if serializer.is_valid():
    #             articles = serializer.save(owner=request.user)
    #             serializers = ArticleSerializer(articles)
    #             print(serializers.data)
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.errors)
    #     else:
    #         return NotAuthenticated


class ArticleDetailView(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
