from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            unique=True,
                            verbose_name='Название ингредиента')
    unit_of_measurement = models.CharField(max_length=200,
                                           verbose_name='единицы измерения')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    title = models.CharField(max_length=200,
                             unique=True,
                             verbose_name='Название тега')
    color = ColorField('Цвет в HEX',
                       default='#FF0000')
    slug = models.SlugField(unique=True, default=title,
                            verbose_name='Уникальный Slug тега')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название блюда')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    description = models.TextField(verbose_name='Рецепт')
    image = models.ImageField(verbose_name='фото блюда',
                              upload_to='base_app/',
                              null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient,
                                         through='AdditionIngredient',
                                         verbose_name='Ингредиенты',
                                         )
    tags = models.ManyToManyField(Tag,
                                  verbose_name='тег',
                                  )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления, в мин')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class AdditionIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='add_ingredients',
                                   verbose_name='Ингредиент',
                                   )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='add_ingredients',
                               verbose_name='Рецепт',
                               )
    quantity = models.PositiveIntegerField(verbose_name='количество')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='one_ingredients_in_recipe')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь'
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorites',
                               verbose_name='Избранный рецепт'
                               )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f'рецепт {self.recipe} в корзине'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='cart',
                             verbose_name='Пользователь'
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='cart',
                               verbose_name='рецепт'
                               )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_recipe_in_cart')
        ]

    def __str__(self):
        return self.recipe
