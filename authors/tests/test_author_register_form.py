from django.test import TestCase
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