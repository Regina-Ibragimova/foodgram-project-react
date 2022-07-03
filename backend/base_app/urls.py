from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import TagViewSet, IngredientsViewSet, RecipeViewSet

app_name = 'base_app'

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
]
