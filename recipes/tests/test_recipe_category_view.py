from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id':1})
        )
        self.assertIs(view.func, views.category)
    
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """
        Testar se a receita com parametro is_published=False nao e publicada
        """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': recipe.category.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_returns_status_code_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={
                    'category_id':1000
                }
            )
        )
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_category_template_loads_recipes(self):
        required_title = 'Esse é um teste da categoria'

        self.make_recipe(title=required_title)

        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={
                    'category_id':1,
                }
            )
        )
        content = response.content.decode('utf-8')

        self.assertIn(required_title, content)