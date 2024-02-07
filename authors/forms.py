import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError((
            'A senha precisa ter letra, número'
            ' e caracter especial.'
            ),
            code='Inválida'
        )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu usuário')
        add_placeholder(self.fields['email'], 'Seu email')
        add_placeholder(self.fields['first_name'], 'Ex: Maria')
        add_placeholder(self.fields['last_name'], 'Ex: Santos')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['password_confirm'], 'Confirme sua senha')

    username = forms.CharField(
        error_messages={
            'required': 'Esse campo não pode ser vazio',
            'invalid': 'Campo inválido',
            'min_length': 'Usuário precisa ter no mínimo 4 caracteres',
            'max_length': 'Usuário precisa ter no máximo 50 caracteres',
        },
        help_text='O nome de usuário precisa ter letras ou números',
        label='Usuário',
        min_length=4,
        max_length=50,
    )

    first_name = forms.CharField(
        error_messages={
            'required': 'Escreva seu primero nome'
        },
        widget=forms.TextInput(attrs={
            'class': 'input text-input',
        }),
        help_text='Nome social',
        label='Nome',
    )

    last_name = forms.CharField(
        error_messages={
            'required': 'Escreva seu sobrenome'
        },
        label='Sobrenome',
    )

    email = forms.CharField(
        error_messages={
            'required': 'Preencha seu email'
        },
        label='E-mail',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A senha não pode ser vazia'
        },
        help_text=(
            'A senha precisa ter letra, número'
            ' e caracter especial.'
        ),
        validators=[strong_password],
        label='Senha',
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A senha não pode ser vazia'
        },
        label='Repita a senha',
    )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
    
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