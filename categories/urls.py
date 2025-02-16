from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import CategoriViewset

router = DefaultRouter()

router.register('categoryView', CategoriViewset)

urlpatterns = [
    path('', include(router.urls))
]