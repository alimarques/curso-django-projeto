from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
    
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()    # Validacao dos campos

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            title = 'title',
            description = 'description',
            slug = 'slug',
            preparation_time = 1,
            preparation_time_unit = 'preparation_time_unit',
            servings = 5,
            servings_unit = 'servings_unit',
            preparation_steps = 'preparation_steps',
            category = self.make_category(name='Test default'),
            author = self.make_author(username='testauthor'),
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False',
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False',
        )