from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
import uuid


category_choices = [('Заметка', 'Заметка'),
                    ('Ссылка', 'Ссылка'),
                    ('Памятка', 'Памятка'),
                    ('TODO', 'TODO'),
                    ('...', '...')]


class Note(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=1000, verbose_name='заголовок')

    text = RichTextField(max_length=10000, default='', verbose_name='текст')

    created_at = models.DateTimeField(auto_now_add=True)

    category = models.CharField(verbose_name='категория', choices=category_choices, blank=False, null=False,
                                max_length=150, default=('Заметка', 'Заметка'))

    is_chosen_one = models.BooleanField(default=False)

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='автор')

    def __str__(self):
        return '{}. ({})'.format(self.title, self.created_at)
