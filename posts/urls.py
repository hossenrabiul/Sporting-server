from django.urls import path
from . views import PostList, PostDetail, newPostList, newPostDetail
urlpatterns = [
  
    path('postlist/', PostList.as_view(), name = 'postlist'),
    path('postlist/<slug:slug>/', PostList.as_view(), name = 'filter'),

    path('newpostlist/', newPostList.as_view(), name = 'postlist'),
    path('newpostlist/<slug:slug>/', newPostList.as_view(), name = 'filter'),


    path('postdetail/<int:pk>/', PostDetail.as_view(), name = 'postdetail'),
    path('newpostdetail/<int:pk>/', newPostDetail.as_view(), name = 'postdetail'),
]