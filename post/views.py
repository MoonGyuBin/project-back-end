from rest_framework.views import APIView
from rest_framework.response import Response
from post.models import Post
from post.serializers import PostListSerializer,PostCreateSerializer


# Create your views here.

# 게시글 리스트 보기/작성
class PostView(APIView):
    def get(self, request):
        articles = Post.objects.all() 
        serializer = PostListSerializer(articles, many=True) 
        return Response(serializer.data) 

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save(user=request.user) 
            return Response(serializer.data) 
        else:
            return Response(serializer.errors) 
        
