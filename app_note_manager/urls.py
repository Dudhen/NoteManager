from django.urls import path
from .views import NoteListView, NoteDetailView, NoteDeleteView, ChosenOneNoteView, SearchResultsView

urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
    path('<uuid:pk>/', NoteDetailView.as_view(), name='note'),
    path('delete/',  NoteDeleteView.as_view(), name='note_delete'),
    path('chosen-one-note/',  ChosenOneNoteView.as_view(), name='chosen_one_note'),
    path('search-result/',  SearchResultsView.as_view(), name='search_result'),
    # path('protocol/', ProtocolListView.as_view(), name='protocol'),
]
