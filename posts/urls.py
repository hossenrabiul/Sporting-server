from django.urls import path
from . views import PostList, PostDetail
urlpatterns = [
  
    path('postlist/', PostList.as_view(), name = 'postlist'),
    path('postdetail/<int:pk>/', PostDetail.as_view(), name = 'postdetail'),
]