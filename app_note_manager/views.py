import datetime

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
import json
from django.shortcuts import HttpResponse
from django.template import loader, RequestContext
from .forms import FilterNotesForm

from .models import Note
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView


class NoteListView(LoginRequiredMixin, ListView):
    """
    Класс представления журнала работ.
    LoginRequiredMixin - для перенаправления неавторизованных
    пользователей на страницу авторизации
    """
    model = Note
    context_object_name = 'note_list'
    template_name = 'app_note_manager/notes_list.html'
    login_url = 'account_login'
    form_class = FilterNotesForm

    def get_queryset(self):
        """
        Получить отчеты относящиеся только к пользователю
        (!!!но не к контрагенту!!!)
        """
        user = self.request.user

        # обнуляем значение "object_name" в сессии,
        # чтобы при загрузке страницы отображались все объекты
        self.request.session['data_filter'] = False
        self.request.session['sorted_item'] = '-created_at'

        queryset = Note.objects.filter(
            author=user
        ).order_by(
            '-created_at'
        )
        return queryset

    def get_context_data(self, **kwargs):
        """
        Разделить отчеты по объектам для авторизованного пользователя
        """
        # добавляем информацию об объектах в контекст
        # для группировки отчетов на странице
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # получаем названия объектов существующих отчетов
        # object_names = JobLog.objects.filter(
        #     author=user).distinct().values('object_name')
        category_names = [('Все категории', 'Все категории')]
        category_names.extend([
            (note.category, note.category) for note in self.get_queryset()
        ])

        try:
            date_from = Note.objects.filter(
                author=user
            ).earliest('created_at').created_at
            date_by = Note.objects.filter(
                author=user
            ).latest('created_at').created_at
        except Note.DoesNotExist:
            date_from = None
            date_by = None

        # print(date_from)

        # записываем в контекст
        # context["category_names"] = category_names
        context["form"] = self.form_class(category_choices=category_names, date_from=date_from, date_by=date_by)
        return context


class SearchResultsView(LoginRequiredMixin, View):

    def get(self, request):
        user = self.request.user
        sorted_item = request.GET.get('sorted_item', None)
        if sorted_item:
            if request.session.get('sorted_item') == sorted_item:
                sorted_item_queryset = '-{}'.format(sorted_item)
                sorted_flag = "False"
            else:
                sorted_item_queryset = sorted_item
                sorted_flag = "True"
            self.request.session['sorted_item'] = sorted_item_queryset
        else:
            sorted_item = 'created_at'
            sorted_item_queryset = '-{}'.format(sorted_item)
            sorted_flag = "False"

        if request.GET.get('use_filter'):
            data_filter = {'title': request.GET.get('title'),
                           'category': request.GET.get('category'),
                           'date_from': request.GET.get('date_from'),
                           'date_by': request.GET.get('date_by'),
                           'is_chosen_one': request.GET.get('is_chosen_one')}
        else:
            data_filter = request.session.get('data_filter')
        if data_filter:
            self.request.session['data_filter'] = data_filter
            queryset = Note.objects.filter(
                author=user, created_at__gte=datetime.datetime.strptime(data_filter['date_from'], '%Y-%m-%d'),
                created_at__lte=datetime.datetime.strptime(data_filter['date_by'], '%Y-%m-%d') + datetime.timedelta(days=1)
            ).order_by(
                sorted_item_queryset
            )
            if data_filter['title']:
                queryset = queryset.filter(title__icontains=data_filter['title'])
            if data_filter['category'] != 'Все категории':
                queryset = queryset.filter(category=data_filter['category'])
            if data_filter['is_chosen_one'] != 'Все заметки':
                if data_filter['is_chosen_one'] == 'Только избранные':
                    is_chosen_one = True
                else:
                    is_chosen_one = False
                queryset = queryset.filter(is_chosen_one=is_chosen_one)
        else:
            queryset = Note.objects.filter(
                author=user
            ).order_by(
                sorted_item_queryset
            )
        t = loader.get_template('app_note_manager/search_results.html')
        html = t.render({'note_list': queryset, 'sorted_item': sorted_item, 'sorted_flag': sorted_flag})
        return HttpResponse(json.dumps({'html': html}))


class NoteDeleteView(LoginRequiredMixin, View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        Note.objects.get(id=id1).delete()
        data = {
            'deleted': True,
        }
        return JsonResponse(data)


class ChosenOneNoteView(LoginRequiredMixin, View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        note = Note.objects.get(id=id1)
        if note.is_chosen_one:
            is_chosen_one = False
        else:
            is_chosen_one = True
        note.is_chosen_one = is_chosen_one
        note.save()
        data = {
            'is_chosen_one': is_chosen_one
        }
        return JsonResponse(data)


class NoteDetailView(LoginRequiredMixin, DetailView):
    """
    Класс представления информации по определенному отчету.
    """
    model = Note
    context_object_name = 'note'
    template_name = 'app_note_manager/notes_detail.html'
    login_url = 'account_login'


class NoteDetailAJAXView(LoginRequiredMixin, View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        obj = Note.objects.get(id=id1)
        t = loader.get_template('app_note_manager/notes_detail.html')
        html = t.render({'note': obj, 'ajax_flag': True})
        return HttpResponse(json.dumps({'html': html}))
