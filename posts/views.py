from posts.models import Products, newProducts
from posts.serializers import PostSerializer, newPostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import IsAuthorOrReadOnly
from categories.models import Category
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 4
    
class PostList(APIView):
    # permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPagination

    def get(self, request, slug = None):
        print(slug)
        print('PostList  --->> inside get ')
        product = Products.objects.all()
    
        if slug:
            try:
                slug = Category.objects.get(slug = slug)
                product = Products.objects.filter(category = slug)
            except:
                return Response("brand does not exit")
            
        else:
            query = request.GET.get('search', '')
            if query:
                print(query)
                query_product = Products.objects.filter(name__icontains=query)
                if query_product.exists():
                    product = query_product
                else:
                    return Response({'Not found any product'}, status=status.HTTP_404_NOT_FOUND)

        paginator = self.pagination_class()
        paginator_queryset = paginator.paginate_queryset(product, request)

        data = PostSerializer(paginator_queryset, many = True).data
        return paginator.get_paginated_response(data)
    
    def post(self, request, format=None):
        print('PostList  --->> inside post ')
        # print(request.data)
        # if not request.user.is_authenticated:
        #     return Response({'error': 'Authentication required'}, status=401)
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class newPostList(APIView):
  
    # permission_classes = [IsAuthorOrReadOnly]
    
    def get(self, request, slug = None):
        print(slug)
        print('PostList  --->> inside get ')
        product = newProducts.objects.all()
        if slug:
            try:
                slug = Category.objects.get(slug = slug)
                product = Products.objects.filter(category = slug)
            except:
                return Response("brand does not exit")

        data = newPostSerializer(product, many = True).data
        return Response(data)
        
    def post(self, request, format=None):
        print('PostList  --->> inside post ')
        print(request.data)
        # if request.user.is_anonymous:
        #     return Response({'error': 'Authentication required'}, status=401)
        
        serializer = newPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ProductsByCategory(generics.ListAPIView):
#     serializer_class = PostSerializer  # Use PostSerializer

#     def get_queryset(self):
#         category_slug = self.kwargs.get('slug')  # Get category slug from URL
#         category = get_object_or_404(Category, slug=category_slug)  # Get category object
#         return Products.objects.filter(category=category)
    

class PostDetail(APIView):
    """
    Retrieve, update or delete a post instance.
    """
    
    # permission_classes = [IsAuthorOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class newPostDetail(APIView):
    """
    Retrieve, update or delete a post instance.
    """
    
    # permission_classes = [IsAuthorOrReadOnly]
    
    def get_object(self, pk):
        try:
            return newProducts.objects.get(pk=pk)
        except newProducts.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = newPostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = newPostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)