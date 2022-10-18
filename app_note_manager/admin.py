from django.contrib import admin
from allauth.account.models import EmailAddress
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    """
    Административная панель заметки
    """
    list_display = (
        "title",
        "short_text",
        "category",
        "created_at",
        "is_chosen_one",
        "get_author"
    )

    list_filter = ('author', 'category')
    search_fields = ('title',)

    def short_text(self, obj):
        """
        Функция возвращающая первые 15 символов
        текста заметки в административной панель
        """
        if len(obj.text) > 15:
            return obj.text[:15] + '...'
        else:
            return obj.text

    def get_author(self, obj):
        """
        Функция для отображения автора заметки
        """
        return obj.author.username

    short_text.short_description = 'текст'
    get_author.short_description = 'автор'


admin.site.register(Note, NoteAdmin)
admin.site.unregister(EmailAddress)
