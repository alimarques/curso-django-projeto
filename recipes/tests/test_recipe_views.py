from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):    
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:home')
        )
        self.assertIs(view.func, views.home)
    
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Nenhuma receita por enquanto',
            response.content.decode('utf-8')
        )
    
    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))

        # Checar se uma receita existe
        self.assertEqual(len(response.context['recipes']), 1)
    
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """
        Testar se a receita com parametro is_published=False nao e publicada
        """
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'Nenhuma receita por enquanto',
            response.content.decode('utf-8')
        )

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

    def test_recipe_search_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:search')
        )
        self.assertIs(view.func, views.search)

    def test_recipe_search_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
    
    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=<teste>')
        self.assertIn(
            'Pesquisa por &quot;&lt;teste&gt;&quot;',
            response.content.decode('utf-8')
        )