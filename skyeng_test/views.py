from django.shortcuts import redirect


def page_not_found_view(request, exception):
    """
    Функция для перенаправления авторизованного пользователя
    на страницу со списком заметок, а неавторизованного - на страницу входа
    (Работает только когда в настройках DEBUG = False)
    """
    return redirect('note_list')
