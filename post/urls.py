from django.urls import path
from post import views

urlpatterns = [

    path('', views.PostView.as_view(), name='PostView'),  # 전체 게시글
    path("article/", views.ArticleView.as_view(), name="ArticleView"), 
    path("article/<int:pk>", views.ArticleDetailView.as_view(),
         name="ArticleDetailView"),

]
