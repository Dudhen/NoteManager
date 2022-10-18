from app_note_manager.models import Note


def get_filters_form_attributes(user):

    notes = Note.objects.filter(
        author=user
    ).order_by(
        '-created_at'
    )

    category_names = [('Все категории', 'Все категории')]
    category_names.extend(list(set([
        (note.category, note.category) for note in notes
    ])))

    try:
        date_from = Note.objects.filter(
            author=user
        ).earliest('created_at').created_at.date().strftime('%Y-%m-%d')
        date_by = Note.objects.filter(
            author=user
        ).latest('created_at').created_at.date().strftime('%Y-%m-%d')
    except Note.DoesNotExist:
        date_from = None
        date_by = None

    return {'category_names': category_names, 'date_from': date_from, 'date_by': date_by}