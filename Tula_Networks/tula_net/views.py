from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import FeederFormAdd, FeederFormUpd, PhoneSubscriberFormAdd, PhonePersonFormAdd, PhoneFormUpd, \
    PhonePSFormAdd, SubscriberFormAdd, PersonFormAdd, SubstationFormUpd
from .models import Substation, Subscriber, Section, Person, Phone, Feeder, Group, Res
from dal import autocomplete

from .utils import AddPhoneViewMixin, DeleteObjectMixin

title = 'Тульские Сети'
context_menu = {'substations': 'Подстанции', 'subscribers': 'Абоненты', 'persons': 'Ответственные лица', }

# context_menu = {'substations': 'Подстанции', 'subscribers': 'Абоненты', 'feeders': 'Присоединения',
#             'persons': 'Ответственные лица', 'sections': 'Секции', 'phones': 'Телефоны'}

title1 = {'title': title}
context2 = {'context_menu': context_menu, 'title': title}


class Main(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tula_net/index.html', context=context2)


class PsList(ListView):
    """ все ПС """
    model = Substation
    context_object_name = 'substations'
    template_name = 'tula_net/listPS.html'
    extra_context = title1
    """ context['groups'] - меню в верху страницы с названиями групп ПС 
    ['flag_group'] - для того чтобы не выводить названия групп, если группа уже выбрана и убрать поле поиска """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        context['groups'] = Group.objects.all()
        context['voltages'] = [35, 110, 220]
        return context


class GroupPS(ListView):
    """ ПС по группам """
    context_object_name = 'substations'
    template_name = 'tula_net/listPS.html'

    def get_queryset(self):
        return Substation.objects.filter(group__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['voltages'] = [35, 110, 220]
        context['flag_group'] = 1

        return context


class VoltPS(ListView):
    """ ПС по группам """
    context_object_name = 'substations'
    template_name = 'tula_net/listPS.html'

    def get_queryset(self):
        return Substation.objects.filter(voltage_h=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voltages'] = [35, 110, 220]
        context['groups'] = Group.objects.all()
        context['flag_voltages'] = 1
        return context


class SubstationsBySubscriber(ListView):
    """ ПС по по абонентам со списком фидеров """

    context_object_name = 'substations'
    template_name = 'tula_net/substations_by_ss.html'

    def get_queryset(self):
        return Substation.objects.filter(feeders__subscriber__pk=self.kwargs['pk'])

    """ context['the_subscriber'] - тот абонент для которого выводятся ПС и фидера """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_subscriber'] = Subscriber.objects.get(pk=self.kwargs['pk'])
        context['context_menu'] = context_menu
        return context


class ResPS(ListView):
    pass


class OnePS(DetailView):
    """ карточка одной пс """
    model = Substation
    template_name = 'tula_net/onePS.html'
    context_object_name = 'ps'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


class SectionList(ListView):
    """ все секции с фидерами - бесполезная) """
    model = Section
    template_name = 'tula_net/section.html'
    context_object_name = 'sections'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


class OneFeeders(DetailView):
    model = Feeder
    template_name = 'tula_net/feeder.html'
    context_object_name = 'feeder'


class AllFeeders(ListView):
    model = Feeder
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


# одна секция - лист фидеров
class OneSection(ListView):
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'

    def get_queryset(self):
        return Feeder.objects.filter(section__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_section'] = Section.objects.get(pk=self.kwargs['pk'])
        context['context_menu'] = context_menu
        return context


class OneSubstation(ListView):
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'

    def get_queryset(self):
        return Feeder.objects.filter(substation__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_substation'] = Substation.objects.get(pk=self.kwargs['pk'])
        context['context_menu'] = context_menu
        return context


class SectionPS(ListView):
    template_name = 'tula_net/section.html'
    context_object_name = 'sections'

    def get_queryset(self):
        return Section.objects.filter(substation__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_substation'] = Substation.objects.get(pk=self.kwargs['pk'])
        context['context_menu'] = context_menu
        return context


class OneSubscriber(DetailView):
    model = Subscriber
    template_name = 'tula_net/one_subscriber.html'
    context_object_name = 'subscriber'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


class SubscriberList(ListView):
    model = Subscriber
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers_all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubscribersBySection(ListView):
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers.html'

    def get_queryset(self):
        return Subscriber.objects.filter(feeders__section__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_section'] = Section.objects.get(pk=self.kwargs['pk'])
        return context


class SubscribersByPS(ListView):
    """ одна ПС со списком всех абонентов +
    все абоненты со списком всех фидеров по ЭТОЙ ПС """
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers.html'

    def get_queryset(self):
        return Subscriber.objects.filter(feeders__substation__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_substation'] = Substation.objects.get(pk=self.kwargs['pk'])
        return context


# _________________ люди __________________
class PersonList(ListView):
    """ список всех людей """
    model = Person
    template_name = 'tula_net/persons.html'
    context_object_name = 'persons'


class OnePerson(DetailView):
    """ один человек """
    model = Person
    template_name = 'tula_net/one_person.html'
    context_object_name = 'person'


# ____________ телефоны _______________
class PhoneList(ListView):
    model = Phone
    template_name = 'tula_net/phones.html'
    context_object_name = 'phones'


class OnePhone(DetailView):
    """ один телефон """
    model = Phone
    template_name = 'tula_net/one_phone.html'
    context_object_name = 'phone'


# __________________ Поиски ____________________
class SearcherSubscribers(ListView):
    """ Поиск по абонентам """
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers_all.html'

    def get_queryset(self):
        return Subscriber.objects.filter(
            Q(name__icontains=self.request.GET.get('s')) |
            Q(short_name__icontains=self.request.GET.get('s')) |
            Q(name__icontains=self.request.GET.get('s').title()) |
            Q(short_name__icontains=self.request.GET.get('s').title().upper())
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_search'] = self.request.GET.get('s')
        return context


class SearcherPS(ListView):
    """ Поиск по подстанциям """
    context_object_name = 'substations'
    template_name = 'tula_net/listPS.html'

    def get_queryset(self):
        return Substation.objects.filter(
            Q(name__icontains=self.request.GET.get('s')) |
            Q(name__icontains=self.request.GET.get('s').title()) |
            Q(name__icontains=self.request.GET.get('s').lower())
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_search'] = self.request.GET.get('s')
        context['groups'] = Group.objects.all()

        context['flag_group'] = 1
        return context


class SearcherPersons(ListView):
    """ Поиск по людям """
    context_object_name = 'persons'
    template_name = 'tula_net/persons.html'

    def get_queryset(self):
        return Person.objects.filter(
            Q(name__icontains=self.request.GET.get('s')) |
            Q(name__icontains=self.request.GET.get('s').title()) |
            Q(name__icontains=self.request.GET.get('s').lower())
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_search'] = self.request.GET.get('s')
        return context


class SearcherPhones(ListView):
    """ Поиск по телефонам """
    context_object_name = 'phones'
    template_name = 'tula_net/phones.html'

    def get_queryset(self):
        return Phone.objects.filter(
            Q(number__contains=self.request.GET.get('s')) |
            Q(search_number__contains=self.request.GET.get('s')) |
            Q(mail__icontains=self.request.GET.get('s'))
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_search'] = self.request.GET.get('s')
        return context


# ___________________ ФОРМЫ ____________________
## __________________ фидеры ____________________
class AddFeeder(View):
    """ добавление фидера!!! и оно работает !!!"""

    def get(self, request, *args, **kwargs):
        form = FeederFormAdd()
        form.fields["substation"].queryset = Substation.objects.filter(pk=self.kwargs['pk'])
        form.fields["section"].queryset = Section.objects.filter(substation__pk=self.kwargs['pk'])
        return render(request, 'tula_net/form_add_feeder.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        bound_form = FeederFormAdd(request.POST)
        if bound_form.is_valid():
            new_feeder = bound_form.save()
            return redirect(new_feeder)
        return render(request, 'tula_net/form_add_feeder.html', context={'form': bound_form})


class UpdFeeder(UpdateView):
    """ изменение фидера"""
    form_class = FeederFormUpd
    model = Feeder
    template_name = 'tula_net/form_add_feeder.html'


## __________________ телефоны ____________________


class AddSubscriberPhone(AddPhoneViewMixin, View):
    """ добавление телефона организации"""
    model = Subscriber
    form_x = PhoneSubscriberFormAdd


class AddPersonPhone(AddPhoneViewMixin, View):
    """ добавление телефона лица"""
    model = Person
    form_x = PhonePersonFormAdd


class AddPSPhone(AddPhoneViewMixin, View):
    """ добавление телефона ПС"""
    model = Substation
    form_x = PhonePSFormAdd


class UpdPhone(UpdateView):
    """ изменение телефона"""
    form_class = PhoneFormUpd
    model = Phone
    template_name = 'tula_net/form_add_phone.html'


class PhoneDelete(DeleteObjectMixin, View):
    """ удаление телефона"""
    model = Phone
    target_reverse = 'phones'


class FeederDelete(DeleteObjectMixin, View):
    """ удаление фидера"""
    model = Feeder
    target_reverse = 'main'


# _______________ Формы Организации _____________
class AddSubscriber(CreateView):
    """ добавление организации"""
    model = Subscriber
    form_class = SubscriberFormAdd
    template_name = 'tula_net/form_add_subscriber.html'


class UpdSubscriber(UpdateView):
    """ изменение организации"""
    model = Subscriber
    form_class = SubscriberFormAdd
    template_name = 'tula_net/form_add_subscriber.html'


class SubscriberDelete(DeleteObjectMixin, View):
    """ удаление организации"""
    model = Subscriber
    target_reverse = 'subscribers'


# _______________ Формы Организации _____________
class AddPerson(View):

    def get(self, request, *args, **kwargs):
        form = PersonFormAdd()
        form.fields["subscriber"].queryset = Subscriber.objects.filter(pk=self.kwargs['pk'])
        return render(request, 'tula_net/form_add_person.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        bound_form = PersonFormAdd(request.POST)
        if bound_form.is_valid():
            new_person = bound_form.save()
            return redirect(new_person)
        return render(request, 'tula_net/form_add_person.html', context={'form': bound_form})


class UpdPerson(UpdateView):
    model = Person
    form_class = PersonFormAdd
    template_name = 'tula_net/form_add_person.html'


class DelPerson(DeleteObjectMixin, View):
    model = Person
    target_reverse = 'persons'


# _______________ Формы Подстанции _____________

class UpdSubstation(UpdateView):
    model = Substation
    form_class = SubstationFormUpd
    template_name = 'tula_net/form_add_person.html'










# ___________________
class SubscriberAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Subscriber.objects.none()
        qs = Subscriber.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class SubstationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Substation.objects.none()
        qs = Substation.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
# ________________________
