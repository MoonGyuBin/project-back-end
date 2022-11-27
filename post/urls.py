from django.urls import path
from post import views

urlpatterns = [

    path("article/", views.ArticleView.as_view(), name="ArticleView"),  # 전체 게시글
    path("article/<int:pk>/", views.ArticleDetailView.as_view(),
         name="ArticleDetailView"),  # 게시글 상세 페이지
    path("comment/", views.CommentView.as_view(), name="CommentView"),
    path("comment/<int:author_pk>/",
         views.CommentDetailView.as_view(), name="CommentDetailView"),  # 댓글 수정 삭제 페이지

]
