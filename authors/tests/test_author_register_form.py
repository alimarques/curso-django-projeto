from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex: Maria'),
        ('last_name', 'Ex: Santos'),
        ('username', 'Seu usuário'),
        ('email', 'Seu email'),
        ('password', 'Digite sua senha'),
        ('password_confirm', 'Confirme sua senha'),
    ])
    def test_fields_placeholders_is_correct(self, field, needed_value):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(needed_value, current_placeholder)
    
    @parameterized.expand([
        ('first_name', 'Nome social'),
        ('password', 'A senha precisa ter letra, número e caracter especial.'),
    ])
    def test_fields_help_texts_is_correct(self, field, needed_value):
        form = RegisterForm()
        current_help_text = form[field].help_text
        self.assertEqual(needed_value, current_help_text)
    
    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Usuário'),
        ('email', 'E-mail'),
        ('password', 'Senha'),
        ('password_confirm', 'Repita a senha'),
    ])
    def test_fields_labels_is_correct(self, field, needed_value):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(needed_value, current_label)
    
class AuthorRegisterFormIntegrationTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username':'user',
            'first_name':'first',
            'last_name':'last',
            'email':'email@gmail.com',
            'password':'SenhaTeste123',
            'password_confirm':'SenhaTeste123',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'Esse campo não pode ser vazio'),
        ('password', 'A senha não pode ser vazia'),
        ('password_confirm', 'A senha não pode ser vazia'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))