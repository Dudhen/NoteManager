import datetime

from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.views import View
import json
from django.shortcuts import HttpResponse, render, redirect
from django.template import loader
from .forms import FilterNotesForm, NoteCreatedForm, RegisterUserForm

from .models import Note
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from app_note_manager.models import category_choices
from .scripts import get_filters_form_attributes


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
        context = super().get_context_data(**kwargs)

        user = self.request.user

        filters_form_attributes = get_filters_form_attributes(user)

        if self.get_queryset().count() == 0:
            context["hidden_filterButton"] = True
        context["form"] = self.form_class(category_choices=filters_form_attributes['category_names'],
                                          date_from=filters_form_attributes['date_from'],
                                          date_by=filters_form_attributes['date_by'])
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
        from_detail_page_flag = request.GET.get('from_detail_page_flag', None)
        from_link_flag = request.GET.get('from_link_flag', None)
        if from_detail_page_flag:
            if from_link_flag:
                data = {
                    'from_link_flag': from_link_flag
                }
                return JsonResponse(data)
            else:
                note_list = Note.objects.filter(
                    author=self.request.user
                ).order_by(
                    '-created_at'
                )
                filters_form_attributes = get_filters_form_attributes(self.request.user)
                form = FilterNotesForm(category_choices=filters_form_attributes['category_names'],
                                       date_from=filters_form_attributes['date_from'],
                                       date_by=filters_form_attributes['date_by'])
                t = loader.get_template('app_note_manager/notes_list.html')
                html = t.render({'form': form, 'note_list': note_list})
                return HttpResponse(json.dumps({'html': html}))
        else:
            table_remote = False
            if Note.objects.filter(author=self.request.user).count() == 0:
                table_remote = True
            data = {
                'deleted': True,
                'table_remote': table_remote
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from_link_flag'] = True
        return context


class NoteUpdateView(LoginRequiredMixin, DetailView):
    """
    Класс представления информации по определенному отчету.
    """
    model = Note
    context_object_name = 'note'
    template_name = 'app_note_manager/note_update.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_names'] = category_choices
        context['from_link_flag'] = True
        return context


class NoteDetailAJAXView(LoginRequiredMixin, View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        obj = Note.objects.get(id=id1)
        t = loader.get_template('app_note_manager/notes_detail.html')
        html = t.render({'note': obj})
        return HttpResponse(json.dumps({'html': html}))


class NoteCreateAJAXView(LoginRequiredMixin, View):

    def get(self, request):
        form = NoteCreatedForm
        t = loader.get_template('app_note_manager/note_create.html')
        html = t.render({'form': form})
        if request.GET.get('time_create', None):
            Note.objects.create(title=request.GET.get('title', None),
                                category=request.GET.get('category', None),
                                text=request.GET.get('text', None),
                                author=self.request.user)
            note_list = Note.objects.filter(
                author=self.request.user
            ).order_by(
                '-created_at'
            )
            filters_form_attributes = get_filters_form_attributes(self.request.user)
            form = FilterNotesForm(category_choices=filters_form_attributes['category_names'],
                                   date_from=filters_form_attributes['date_from'],
                                   date_by=filters_form_attributes['date_by'])
            t = loader.get_template('app_note_manager/notes_list.html')
            html = t.render({'form': form, 'note_list': note_list})
        return HttpResponse(json.dumps({'html': html}))


class NoteUpdateAJAXView(LoginRequiredMixin, View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        note = Note.objects.get(id=id1)
        t = loader.get_template('app_note_manager/note_update.html')
        html = t.render({'note': note, 'category_names': category_choices})
        if request.GET.get('save_flag', None):
            from_link_flag = request.GET.get('from_link_flag', None)

            title = request.GET.get('title', None)
            category = request.GET.get('category', None)
            text = request.GET.get('text', None)

            note.title = title
            note.category = category
            note.text = text
            note.save()

            if from_link_flag:
                data = {
                    'from_link_flag': from_link_flag
                }
                return JsonResponse(data)

            t = loader.get_template('app_note_manager/notes_detail.html')
            html = t.render({'note': note})

        return HttpResponse(json.dumps({'html': html}))


class NotePublishAJAXView(LoginRequiredMixin, View):

    def get(self, request):
        id = request.GET.get('id', None)
        current_site = get_current_site(request)
        note_link = 'http://{}/note/{}/update/'.format(current_site, id)
        data = {
            'note_link': note_link
        }
        return JsonResponse(data)


class UserRegister(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    # success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(UserRegister, self).get_context_data(**kwargs)
        context['user_form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        user_form = RegisterUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('note_list')
        else:
            return render(request, self.template_name, {'user_form': user_form})
