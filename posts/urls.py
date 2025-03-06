from django.urls import path
from . views import PostList, PostDetail, ProductsByCategory
urlpatterns = [
  
    path('postlist/', PostList.as_view(), name = 'postlist'),
    path('postlist/<slug:slug>/', PostList.as_view(), name = 'filter'),
    path('postdetail/<int:pk>/', PostDetail.as_view(), name = 'postdetail'),
]