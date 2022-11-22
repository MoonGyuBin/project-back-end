from django.urls import path
from post import views

urlpatterns = [ 
    
    path('', views.PostView.as_view(), name='PostView'), # 전체 게시글

]
