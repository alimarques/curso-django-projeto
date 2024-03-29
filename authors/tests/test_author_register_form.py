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
        ('username', 'O nome de usuário precisa ter letras ou números'),
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
        ('first_name', 'Escreva seu primero nome'),
        ('last_name', 'Escreva seu sobrenome'),
        ('password', 'A senha não pode ser vazia'),
        ('password_confirm', 'A senha não pode ser vazia'),
        ('email', 'Preencha seu email'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        #self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_must_be_4(self):
        self.form_data['username'] = 'Mar'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Usuário precisa ter no mínimo 4 caracteres'
        self.assertIn(msg, response.context['form'].errors.get('username'))
    
    def test_username_field_max_length_must_be_50(self):
        self.form_data['username'] = 'a' * 51
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Usuário precisa ter no máximo 50 caracteres'
        self.assertIn(msg, response.context['form'].errors.get('username'))
    
    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'A senha precisa ter letra, número e caracter especial.'

        self.assertIn(msg, response.context['form'].errors.get('password'))
    
    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = 'Abc@abc123'
        self.form_data['password_confirm'] = 'Abc@abc123!'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'As senhas devem ser idênticas'

        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = 'Abc@abc123'
        self.form_data['password_confirm'] = 'Abc@abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))
    
    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_username_field_contains_only_letters(self):
        self.form_data['first_name'] = 'Luis1'
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)
    
        msg = 'São aceitos somente letras.'

        self.assertIn(msg, response.context['form'].errors.get('first_name'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_dont_contains_reserved_word(self):
        self.form_data['password'] = '123Wos@124senha2'
        self.form_data['password_confirm'] = '123Wos@124senha2'
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)
    
        msg = 'Não digite "senha" na senha'

        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)
    
        msg = 'O email já está em uso.'

        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))
    
    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        self.form_data.update({
            'username': 'testuser',
            'password': 'Abc123456@!',
            'password_confirm': 'Abc123456@!',
        })
        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='Abc123456@!',
        )

        self.assertTrue(is_authenticated)