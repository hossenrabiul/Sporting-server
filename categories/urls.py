from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import CategoriViewset, BrandViewset

router = DefaultRouter()

router.register('categoryView', CategoriViewset)
router.register('brandView', BrandViewset)

urlpatterns = [
    path('', include(router.urls))
]