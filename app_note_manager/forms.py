from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app_note_manager.models import Note


class FilterNotesForm(forms.Form):
    """
    Форма фильтров поиска по заметкам
    """
    category = forms.ChoiceField(choices=[], required=False, label='Категория',)

    title = forms.CharField(required=False, label='Поиск текста в заголовках')

    date_from = forms.DateField(label='Дата "от"', required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_by = forms.DateField(label='Дата "до"', required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    is_chosen_one = forms.ChoiceField(choices=[('Все заметки', 'Все заметки'),
                                               ('Только избранные', 'Только избранные'),
                                               ('Только не избранные', 'Только не избранные')], label='',
                                      required=False, widget=forms.RadioSelect(), initial=('Все заметки', 'Все заметки'))

    def __init__(self, *args, **kwargs):
        """
        Передаем в форму список категорий, а так же
        самую раннюю и самую позднюю даты создания заметки
        """
        # object_choices передается из View
        self.date_from = kwargs.pop('date_from', None)
        self.date_by = kwargs.pop('date_by', None)
        self.category_choices = kwargs.pop('category_choices', None)
        super(FilterNotesForm, self).__init__(*args, **kwargs)
        if self.date_from:
            self.fields['date_from'].initial = self.date_from
        if self.date_by:
            self.fields['date_by'].initial = self.date_by
        if self.category_choices:
            self.fields['category'].choices = self.category_choices


class NoteCreatedForm(forms.ModelForm):
    """
    Форма создания заметки
    """
    class Meta:
        model = Note
        fields = ('title', 'category')


class RegisterUserForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
