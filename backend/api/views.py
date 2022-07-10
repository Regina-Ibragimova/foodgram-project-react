from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import AuthorAndTagFilter, IngredientSearchFilter
from api.pagination import LimitPageNumberPagination
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from api.serializers import (CorrectRecipeSerializer, IngredientSerializer,
                             RecipeSerializer, TagSerializer)
from base_app.models import (Favorite, Ingredient, Recipe,
                             ShoppingCart, Tag)
from api.utils import get_shop_list_pdf_binary


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = AuthorAndTagFilter
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'GET':
            return self.add_obj(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'GET':
            return self.add_obj(ShoppingCart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(ShoppingCart, request.user, pk)
        return None

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Рецепт уже добавлен в список'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = CorrectRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт удален раннее'
        }, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def shop_list_download(request):
        ingredients_sum = {}
        recipes = Recipe.objects.filter(shoppingcart__user=request.user)
        ingredients = recipes.values('ingredient__name',
                                     'ingredient__quantity',
                                     'ingredient__unit_of_measurement',
                                     named=True).order_by(
                                     'ingredient__name').annotate(
            ingredients_total=Sum('ingredient_quantities__quantity')
        )

        for ingredient in ingredients:
            name = ingredient.ingredient__name
            if name not in ingredients_sum:
                ingredients_sum[name] = {
                    'quantity': ingredient.quantity,
                    'dimension': ingredient.ingredient__unit_of_measurement, }
            else:
                ingredients_sum[name]['quantity'] += ingredient.quantity
        return FileResponse(
            get_shop_list_pdf_binary(ingredients_sum),
            filename='Shop_list.pdf',
            as_attachment=True
        )
