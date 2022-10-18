from django.urls import path
from .views import NoteListView, NoteDetailView, NoteDeleteView, ChosenOneNoteView, SearchResultsView, \
    NoteDetailAJAXView, NoteCreateAJAXView, NoteUpdateAJAXView, NotePublishAJAXView, NoteUpdateView

urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
    path('<uuid:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('ajax/note-detail/', NoteDetailAJAXView.as_view(), name='note_detail_ajax'),
    path('delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('chosen-one-note/', ChosenOneNoteView.as_view(), name='chosen_one_note'),
    path('search-result/', SearchResultsView.as_view(), name='search_result'),
    path('note-create/', NoteCreateAJAXView.as_view(), name='note_create'),
    path('note-update/', NoteUpdateAJAXView.as_view(), name='note_update'),
    path('<uuid:pk>/update/', NoteUpdateView.as_view(), name='note_update_link'),
    path('note-publish/', NotePublishAJAXView.as_view(), name='note_publish'),
]
