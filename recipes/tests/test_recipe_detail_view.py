from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):    
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id':1
                }
            )
        )
        self.assertIs(view.func, views.recipe)
    
    def test_recipe_detail_view_returns_status_code_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id':1000
                }
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        required_title = 'Pagina da receita - Carrega uma receita'

        self.make_recipe(title=required_title)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id':1
                }
            )
        )
        content = response.content.decode('utf-8')

        self.assertIn(required_title, content)
    
    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """
        Testar se a receita com parametro is_published=False nao e publicada
        """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id})
        )

        self.assertEqual(response.status_code, 404)