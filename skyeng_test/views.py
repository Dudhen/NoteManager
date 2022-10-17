from django.shortcuts import redirect


def page_not_found_view(request, exception):
    return redirect('note_list')
