from django.contrib import admin
from allauth.account.models import EmailAddress
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "short_text",
        "category",
        "created_at",
        "is_chosen_one",
        "get_author"
    )
    # поля для фильтрации отчетов
    list_filter = ('author', 'category')
    # поля, по которым производится поиск отчетов
    search_fields = ('title',)

    def short_text(self, obj):
        if len(obj.text) > 15:
            return obj.text[:15] + '...'
        else:
            return obj.text

    def get_author(self, obj):
        return obj.author.username

    # mark_as_delete_from_admin.short_description = 'Удалить от имени администратора'
    short_text.short_description = 'текст'
    get_author.short_description = 'автор'

    # получаем контрагента определенного пользователя
    # для отображения в Django-admin
    # def get_contractor(self, obj):
    #     return obj.author.contractor
    #
    # get_contractor.short_description = 'Контрагент'
    # get_contractor.admin_order_field = 'author__contractor'


admin.site.register(Note, NoteAdmin)
admin.site.unregister(EmailAddress)
