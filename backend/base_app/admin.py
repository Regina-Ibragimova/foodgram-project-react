from django.contrib import admin
from .models import Favorite, Recipe, Tag, Ingredient, ShoppingCart


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'author',)
    search_fields = ('tags',)
    list_filter = ('name', 'tags')
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_of_measurement')
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
