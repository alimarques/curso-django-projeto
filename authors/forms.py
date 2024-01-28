import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu usuário')
        add_placeholder(self.fields['email'], 'Seu email')
        add_placeholder(self.fields['first_name'], 'Ex: Maria')
        add_placeholder(self.fields['last_name'], 'Ex: Santos')
        add_placeholder(self.fields['password'], 'Digite sua senha')

    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
        }),
        error_messages={
            'required': 'A senha não pode ser vazia'
        },
        help_text=(
            'A senha precisa ter letra, número'
            ' e caracter especial.'
        )
    )

    labels = {
        'password_confirm': 'Repita a senha',
    }
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Usuário',
            'email': 'E-mail',
            'password': 'Senha',
        }

        help_texts = {
            'first_name': 'Nome social',
        }

        error_messages = {
            'username': {
                'required': 'Esse campo não pode ser vazio',
                'invalid': 'Campo inválido',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input text-input',
            }),
            'password': forms.PasswordInput()
        }
    
    def clean_password(self):
        data = self.cleaned_data.get('password')
        value = 'senha'

        if value in data:
            raise ValidationError(
                f'Não digite "{value}" na senha',
                code='invalid'
            )

        return data
    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        padrao = re.compile(r'[0-9@#$%^&*()_+[\]{}|;:"<>,.?/`~]')
        contains_non_letters = bool(padrao.search(data))

        if contains_non_letters:
            raise ValidationError(
                f'São aceitos somente letras.',
                code='invalid'
            )

        return data
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password_confirm')

        if password != password2:
            password_confirmation_error = 'As senhas devem ser idênticas'
            raise ValidationError({
                'password':password_confirmation_error,
                'password_confirm':password_confirmation_error,
            })