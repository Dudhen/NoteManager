# Generated by Django 4.1.2 on 2022-10-15 15:42

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=1000, verbose_name='заголовок')),
                ('text', ckeditor.fields.RichTextField(default='', max_length=10000, verbose_name='текст')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('Ссылка', 'Ссылка'), ('Заметка', 'Заметка'), ('Памятка', 'Памятка'), ('TODO', 'TODO'), ('...', '...')], max_length=150, verbose_name='категория')),
                ('is_chosen_one', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
        ),
    ]