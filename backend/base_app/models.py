from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            unique=True)
#    quantity = models.PositiveIntegerField()
    unit_of_measurement = models.CharField(max_length=200)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиенты'


class Tag(models.Model):
    title = models.CharField(max_length=200,
                             unique=True,
                             verbose_name='Название тега')
    color = ColorField('Цвет в HEX', default='#FF0000')
    slug = models.SlugField(unique=True, default=title)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Теги'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название блюда')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe',
                               verbose_name='Автор')
    description = models.TextField(verbose_name='Рецепт')
    image = models.ImageField(verbose_name='фото блюда',
                              upload_to='base_app/',
                              null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient,
                                         through='AdditionIngredient',
                                         verbose_name='Ингридиенты',
                                         )
    teg = models.ManyToManyField(Tag,
                                 verbose_name='тег',
                                 )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления, в мин')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепты'

    def __str__(self):
        return self.name


class AdditionIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='add_ingredient',
                                   verbose_name='Ингридиент',
                                   )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='add_ingredient',
                               verbose_name='Рецепт',
                               )
    quantity = models.PositiveIntegerField(verbose_name='количество')

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='one_ingredients_in_recipe')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorite',
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorite',
                               )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'

    def __str__(self):
        return f'рецепт {self.recipe} в корзине'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='cart',
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='cart',
                               )

    def __str__(self):
        return self.recipe


class Follow(models.Model):
    # пользователь, который подписывается
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=None
    )
    # пользователь, на которого подписывются
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='one_following')]

    def __str__(self):
        return f"Последователь: '{self.user}', автор: '{self.author}'"
