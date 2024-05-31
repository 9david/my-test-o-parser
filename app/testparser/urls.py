"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from testparser import views


router = DefaultRouter()
router.register("product", views.ProductViewSet, basename='Product')

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
]
