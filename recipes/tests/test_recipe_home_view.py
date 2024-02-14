from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
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

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_is_paginated(self):
        for i in range(11):
            kwargs = {
                'author_data': {'username':f'u{i}'},
                'slug': f'r{i}',
            }
            self.make_recipe(**kwargs)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 4)
        self.assertEqual(len(paginator.get_page(1)), 3)
    
    def test_invalid_page_query_uses_page_one(self):
        response = self.client.get(reverse('recipes:home') + '?page=1A')
        self.assertEqual(
            response.context['recipes'].number,
            1
        )
        