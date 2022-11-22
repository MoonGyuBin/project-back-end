from rest_framework import serializers
from post.models import Post




# 게시글리스트 보기 GET
class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField() 
   
    def get_user(self, obj): # 유저-> 이메일  
        return obj.user.email 

    class Meta:
        model = Post 
        fields = ('pk','title','image','update_at','user',) # pk = id 


# 게시글 작성 POST
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'image', 'content') 


