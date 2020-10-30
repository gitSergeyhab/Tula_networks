from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import forms

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import FeederAddFromPSForm, FeederFormUpd, PhoneSubscriberFormAdd, PhonePersonFormAdd, PhoneFormUpd, \
    PhonePSFormAdd, SubscriberFormAdd, PersonFormAdd, SubstationFormUpd, FeederAddFromSubscriberForm, SectionAddForm, \
    Line1Form, UserAutForm

from .models import Substation, Subscriber, Section, Person, Phone, Feeder, Group, Region, \
    ClassVoltage, GroupLine, Line
from dal import autocomplete

from .utils import AddPhoneViewMixin, DeleteObjectMixin, SubstationsViewMixin, FeedersViewMixin, AddFeederMixin, \
    chang_search, make_digits, Lines1ViewMixin, SearchMixin, try_int


# from .data import context_menu


class MainView(View):
    """ главная """

    def get(self, request, *args, **kwargs):
        return render(request, 'tula_net/index.html')


class PsListView(SubstationsViewMixin, ListView):
    """ вьюха для всех ПС """
    paginate_by = 20


class GroupPSView(SubstationsViewMixin, ListView):
    """ вьюха для ПС с разбивкой по группе """
    flag = 'flag_group'

    def get_queryset(self):
        return Substation.objects.select_related('group', 'voltage_h', 'voltage_m', 'voltage_l'). \
            filter(group__pk=self.kwargs['pk'])


class VoltPSView(SubstationsViewMixin, ListView):
    """ вьюха для ПС с разбивкой по напряжению """
    flag = 'flag_voltages'
    paginate_by = 20

    def get_queryset(self):
        return Substation.objects.select_related('group', 'voltage_h', 'voltage_m', 'voltage_l'). \
            filter(voltage_h__class_voltage=self.kwargs['pk'])


class SubstationsBySubscriberView(ListView):
    """ ПС по по абонентам со списком фидеров """

    context_object_name = 'substations'
    template_name = 'tula_net/substations_by_ss.html'

    def get_queryset(self):
        return Substation.objects.filter(feeders__subscriber__pk=self.kwargs['pk']). \
            prefetch_related('feeders', 'feeders__subscriber', 'feeders__section__voltage')

    """ context['the_subscriber'] - тот абонент для которого выводятся ПС и фидера """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_subscriber'] = Subscriber.objects.get(pk=self.kwargs['pk'])
        return context


class ResPS(ListView):
    pass


class OnePSView(DetailView):
    """ карточка одной пс """

    template_name = 'tula_net/one_ps.html'
    context_object_name = 'ps'

    def get_queryset(self):
        return Substation.objects.select_related('group', 'voltage_h', 'voltage_m', 'voltage_l'). \
            prefetch_related('sections', 'feeders', 'sections__voltage', 'phones', 'sections__feeders')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lines'] = Line.objects.filter(
            Q(ps_p1=self.object.number) |
            Q(ps_p2=self.object.number) |
            Q(ps_m1=self.object.number) |
            Q(ps_m2=self.object.number) |
            Q(ps_m3=self.object.number) |
            Q(ps_m4=self.object.number)
        ).select_related('voltage')
        return context


class SectionListView(ListView):
    """ все секции с фидерами - бесполезная) """
    # model = Section
    template_name = 'tula_net/section.html'
    context_object_name = 'sections'

    def get_queryset(self):
        return Section.objects.prefetch_related('feeders').select_related('voltage', 'substation').all()

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['context_menu'] = context_menu
    #     return context


# ____________фидера_____________
class OneFeedersView(DetailView):
    template_name = 'tula_net/feeder.html'
    context_object_name = 'feeder'

    def get_queryset(self):
        return Feeder.objects.select_related('subscriber', 'section', 'substation'). \
            prefetch_related('subscriber__phones', 'subscriber__persons__phones').all()


class AllFeedersView(FeedersViewMixin, ListView):
    """ все фидера вообще и сразу """
    paginate_by = 10


class OneSubstationView(FeedersViewMixin, ListView):
    """ одна ПС - лист фидеров """
    second_model = Substation
    the_context = 'the_substation'

    def get_queryset(self):
        return Feeder.objects.select_related('substation', 'section', 'subscriber', 'section__voltage'). \
            filter(substation__pk=self.kwargs['pk'])


# __________ секции _____________
class OneSectionView(FeedersViewMixin, ListView):
    """ одна секция - лист фидеров """
    second_model = Section
    the_context = 'the_section'

    def get_queryset(self):
        return Feeder.objects.select_related('substation', 'section', 'subscriber', 'section__voltage'). \
            filter(section__pk=self.kwargs['pk'])


class Section1View(DetailView):
    """ одна секция - объект """
    context_object_name = 'section'
    template_name = 'tula_net/one_section.html'

    def get_queryset(self):
        return Section.objects.prefetch_related('feeders', 'voltage', 'substation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """линии по секциям - можно проще, но 400 кверис при добавлении объекта ВЛ........"""
        context['lines'] = Line.objects.filter(
            Q(ps_p1=self.object.substation.number, sec_p1=self.object.number, voltage=self.object.voltage) |
            Q(ps_p2=self.object.substation.number, sec_p2=self.object.number, voltage=self.object.voltage) |
            Q(ps_m1=self.object.substation.number, sec_m1=self.object.number, voltage=self.object.voltage) |
            Q(ps_m2=self.object.substation.number, sec_m2=self.object.number, voltage=self.object.voltage) |
            Q(ps_m3=self.object.substation.number, sec_m3=self.object.number, voltage=self.object.voltage) |
            Q(ps_m4=self.object.substation.number, sec_m4=self.object.number, voltage=self.object.voltage)
        )
        return context


# _________ организации _____________
class OneSubscriberView(DetailView):
    template_name = 'tula_net/one_subscriber.html'
    context_object_name = 'subscriber'

    def get_queryset(self):
        return Subscriber.objects.prefetch_related('phones', 'persons', 'persons__phones', 'substations', 'lines')


class SubscriberListView(ListView):
    model = Subscriber
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers_all.html'
    paginate_by = 40

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubscribersBySectionView(ListView):
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers.html'

    def get_queryset(self):
        return Subscriber.objects.prefetch_related(
            'phones', 'persons', 'persons__phones', 'feeders',
            'feeders__substation', 'feeders__section', 'feeders__section__voltage'
        ).filter(feeders__section__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_section'] = Section.objects.select_related('substation').get(pk=self.kwargs['pk'])
        return context


class SubscribersByPSView(ListView):
    """ одна ПС со списком всех абонентов +
    все абоненты со списком всех фидеров по ЭТОЙ ПС """
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers.html'

    def get_queryset(self):
        return Subscriber.objects.prefetch_related(
            'phones', 'persons', 'persons__phones', 'feeders',
            'feeders__substation', 'feeders__section', 'feeders__section__voltage'
        ).filter(feeders__substation__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_substation'] = Substation.objects.get(pk=self.kwargs['pk'])
        return context


# _________________ люди __________________
class PersonListView(ListView):
    """ список всех людей """
    template_name = 'tula_net/persons.html'
    context_object_name = 'persons'
    paginate_by = 24

    def get_queryset(self):
        return Person.objects.select_related('subscriber')


class OnePersonView(DetailView):
    """ один человек """
    model = Person
    template_name = 'tula_net/one_person.html'
    context_object_name = 'person'

    def get_queryset(self):
        return Person.objects.select_related('subscriber').prefetch_related('phones', 'subscriber__phones')


# ____________ телефоны _______________
class PhoneListView(ListView):
    template_name = 'tula_net/phones.html'
    context_object_name = 'phones'
    paginate_by = 32

    def get_queryset(self):
        return Phone.objects.select_related('subscriber', 'person', 'substation')


class OnePhoneView(DetailView):
    """ один телефон """
    template_name = 'tula_net/one_phone.html'
    context_object_name = 'phone'

    def get_queryset(self):
        return Phone.objects.select_related('subscriber', 'person', 'substation'). \
            prefetch_related('person__phones', 'subscriber__phones', 'substation__phones')


# __________________ Поиски ____________________
class SearcherSubscribersView(SearchMixin, ListView):
    """ Поиск по абонентам """
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers_all.html'
    paginate_by = 20

    def get_queryset(self):
        return Subscriber.objects.filter(
            Q(name__icontains=self.request.GET.get('s')) |
            Q(short_name__icontains=self.request.GET.get('s')) |
            Q(name__icontains=self.request.GET.get('s').title()) |
            Q(short_name__icontains=self.request.GET.get('s').title().upper())
        )


class SearcherPSView(ListView):
    """ Поиск по подстанциям """
    context_object_name = 'substations'
    template_name = 'tula_net/substations.html'
    paginate_by = 20

    def get_queryset(self):
        name = self.request.GET.get('s')
        return Substation.objects.select_related('group', 'voltage_h', 'voltage_m', 'voltage_l').filter(
            Q(name__icontains=name) |
            Q(name__icontains=name.title()) |
            Q(name__icontains=name.lower()) |
            Q(number=try_int(name))
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['flag_search'] = self.request.GET.get('s')
        context['groups'] = Group.objects.all()
        context['voltages'] = [35, 110, 220]
        return context


class SearcherPersonsView(SearchMixin, ListView):
    """ Поиск по людям """
    context_object_name = 'persons'
    template_name = 'tula_net/persons.html'
    paginate_by = 18

    def get_queryset(self):
        return Person.objects.select_related('subscriber').filter(
            Q(name__icontains=self.request.GET.get('s')) |
            Q(name__icontains=self.request.GET.get('s').title()) |
            Q(name__icontains=self.request.GET.get('s').lower())
        )


class SearcherPhonesView(SearchMixin, ListView):
    """ Поиск по телефонам """
    context_object_name = 'phones'
    template_name = 'tula_net/phones.html'
    paginate_by = 20

    def get_queryset(self):
        digits = make_digits(self.request.GET.get('s'))
        return Phone.objects.select_related('subscriber', 'substation', 'person').filter(
            Q(number__icontains=self.request.GET.get('s')) |
            Q(search_number__icontains=digits)
        )


class SearcherLinesView(ListView):
    """ Поиск по линиям """
    context_object_name = 'lines'
    template_name = 'tula_net/lines1.html'

    def get_queryset(self):
        obj_serch = self.request.GET.get('s')
        obj_serch_n = chang_search(obj_serch)
        return Line.objects.select_related('management', 'voltage', 'group').filter(
            Q(full_name__icontains=obj_serch) |
            Q(full_name__icontains=obj_serch.title()) |
            Q(name__icontains=obj_serch) |
            Q(name__icontains=obj_serch.title()) |
            Q(short_name__icontains=obj_serch) |
            Q(short_name__icontains=obj_serch_n)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['flag_search'] = self.request.GET.get('s')
        context['groups'] = GroupLine.objects.all()
        context['voltages'] = ClassVoltage.objects.all()[1:3]
        context['regions'] = Region.objects.filter(for_menu=True)
        return context

class FeedersView(ListView):
    context_object_name = 'feeders'
    template_name = 'tula_net/feeder_search.html'
    paginate_by = 28

    def get_queryset(self):
        return Feeder.objects.select_related('substation', 'section', 'subscriber', 'section__voltage')

class SearcherFeedersView(SearchMixin, ListView):
    context_object_name = 'feeders'
    template_name = 'tula_net/feeder_search.html'
    paginate_by = 20

    def get_queryset(self):
        return Feeder.objects.filter(
            Q(name__icontains=self.request.GET.get('s')) |
            Q(name__icontains=self.request.GET.get('s').title()) |
            Q(name__icontains=self.request.GET.get('s').lower())
        ).select_related('substation', 'subscriber')


# ___________________ ФОРМЫ ____________________
## __________________ фидеры ____________________
class AddFeederFromPSView(AddFeederMixin, View):
    """ добавление с ПС """
    form_feeder = FeederAddFromPSForm
    first_model = Substation
    first_field = 'substation'
    second_field = 'section'


class AddFeederFromSecView(AddFeederMixin, View):
    """ добавление с СкШ """
    form_feeder = FeederAddFromPSForm
    first_model = Section
    first_field = 'section'
    second_field = 'substation'


class AddFeederFromSubscriberView(AddFeederMixin, View):
    """ добавление от организации """
    form_feeder = FeederAddFromSubscriberForm
    first_model = Subscriber
    first_field = 'subscriber'


class UpdFeederView(View):
    """ изменение фидера"""

    def get(self, request, pk):
        feeder = Feeder.objects.get(pk=pk)
        form = FeederFormUpd(instance=feeder)
        form.fields['section'].queryset = Section.objects.\
            filter(substation__feeders__pk=pk, voltage__class_voltage__lt=11)
        form.fields['substation'].queryset = Substation.objects.filter(feeders__pk=pk)
        return render(request, 'tula_net/form_add_feeder.html', context={'form': form})

    def post(self, request, pk):
        feeder = Feeder.objects.get(pk=pk)
        form = FeederFormUpd(request.POST, instance=feeder)
        if form.is_valid():
            feeder = form.save()
            return redirect(feeder)
        return render(request, 'tula_net/form_add_feeder.html', context={'form': form})


## __________________ телефоны ____________________


class AddSubscriberPhoneView(AddPhoneViewMixin, View):
    """ добавление телефона организации"""
    model = Subscriber
    form_x = PhoneSubscriberFormAdd


class AddPersonPhoneView(AddPhoneViewMixin, View):
    """ добавление телефона лица"""
    model = Person
    form_x = PhonePersonFormAdd


class AddPSPhoneView(AddPhoneViewMixin, View):
    """ добавление телефона ПС"""
    model = Substation
    form_x = PhonePSFormAdd


class UpdPhoneView(View):
    """ добавление телефона"""

    def get(self, request, pk):
        phone = Phone.objects.get(pk=pk)
        form = PhoneFormUpd(instance=phone)
        form.fields['search_number'].widget = forms.HiddenInput()
        return render(request, 'tula_net/form_add_phone.html', context={'form': form})

    def post(self, request, pk):
        phone = Phone.objects.get(pk=pk)
        bound_form = PhoneFormUpd(request.POST, instance=phone)
        if bound_form.is_valid():
            new_phone = bound_form.save()
            return redirect(new_phone)
        return render(request, 'tula_net/form_add_phone.html', context={'form': bound_form})





class PhoneDeleteView(DeleteObjectMixin, View):
    """ удаление телефона"""
    model = Phone
    target_reverse = 'phones'


class FeederDeleteView(DeleteObjectMixin, View):
    """ удаление фидера"""
    model = Feeder
    target_reverse = 'main'


# _______________ Формы Организации _____________
class AddSubscriberView(CreateView):
    """ добавление организации"""
    model = Subscriber
    form_class = SubscriberFormAdd
    template_name = 'tula_net/form_add_subscriber.html'


class UpdSubscriberView(UpdateView):
    """ изменение организации"""
    model = Subscriber
    form_class = SubscriberFormAdd
    template_name = 'tula_net/form_add_subscriber.html'


class SubscriberDeleteView(DeleteObjectMixin, View):
    """ удаление организации"""
    model = Subscriber
    target_reverse = 'subscribers'


# _______________ Формы Организации _____________
class AddPersonView(View):

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


class UpdPersonView(UpdateView):
    model = Person
    form_class = PersonFormAdd
    template_name = 'tula_net/form_add_person.html'


class DelPersonView(DeleteObjectMixin, View):
    model = Person
    target_reverse = 'persons'


# _______________ Формы Подстанции _____________

class AddSubstationView(CreateView):
    model = Substation
    form_class = SubstationFormUpd
    template_name = 'tula_net/form_add_person.html'


class UpdSubstationView(UpdateView):
    model = Substation
    form_class = SubstationFormUpd
    template_name = 'tula_net/form_add_person.html'


class AddSectionFromPSView(View):
    """ добавление фидера c ПС !!! и оно работает !!!"""

    def get(self, request, pk):
        form = SectionAddForm()
        form.fields["substation"].queryset = Substation.objects.filter(pk=pk)
        return render(request, 'tula_net/form_add_feeder.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        bound_form = SectionAddForm(request.POST)
        if bound_form.is_valid():
            new_feeder = bound_form.save()
            return redirect(new_feeder)
        return render(request, 'tula_net/form_add_feeder.html', context={'form': bound_form})


class UpdSectionView(UpdateView):
    model = Section
    form_class = SectionAddForm
    template_name = 'tula_net/form_add_feeder.html'


class SectionDeleteView(DeleteObjectMixin, View):
    """ удаление секции"""
    model = Section
    target_reverse = 'main'


# ___________________
"""
class SubscriberAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Subscriber.objects.none()
        qs = Subscriber.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class SubstationAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Substation.objects.none()
        qs = Substation.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

"""
# ________________________

# class LinesView(LinesViewMixin, ListView):
#     paginate_by = 12


class Lines1View(Lines1ViewMixin, ListView):
    paginate_by = 12


class LinesGroupView(Lines1ViewMixin, ListView):
    flag = 'flag_group'
    paginate_by = 12

    def get_queryset(self):
        return Line.objects.select_related('management', 'voltage', 'group'). \
            filter(group__pk=self.kwargs['pk'])


class LinesVoltageView(Lines1ViewMixin, ListView):
    flag = 'flag_voltages'
    paginate_by = 12

    def get_queryset(self):
        return Line.objects.select_related('management', 'voltage', 'group'). \
            filter(voltage__pk=self.kwargs['pk'])


class LinesRegionView(Lines1ViewMixin, ListView):
    flag = 'flag_region'
    paginate_by = 12

    def get_queryset(self):
        return Line.objects.select_related('management', 'voltage', 'group'). \
            filter(management__pk=self.kwargs['pk'])


class OneLine1View(DetailView):
    model = Line
    context_object_name = 'line'
    template_name = 'tula_net/one_line1.html'

    def get_queryset(self):
        return Line.objects.select_related('voltage', 'group', 'voltage', 'subscriber', 'management'). \
            prefetch_related('maintenance')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plus'] = Section.objects.select_related('substation'). \
            filter(Q(substation__number=self.object.ps_p1, number=self.object.sec_p1, voltage=self.object.voltage) |
                   Q(substation__number=self.object.ps_p2, number=self.object.sec_p2, voltage=self.object.voltage))

        context['minus'] = Section.objects.select_related('substation'). \
            filter(Q(substation__number=self.object.ps_m1, number=self.object.sec_m1, voltage=self.object.voltage) |
                   Q(substation__number=self.object.ps_m2, number=self.object.sec_m2, voltage=self.object.voltage) |
                   Q(substation__number=self.object.ps_m3, number=self.object.sec_m3, voltage=self.object.voltage) |
                   Q(substation__number=self.object.ps_m4, number=self.object.sec_m4, voltage=self.object.voltage)
                   )
        return context


class AddLine1View(View):
    """ добавление фидера c ПС !!! и оно работает !!!"""

    def get(self, request):
        form = Line1Form()
        form.fields['voltage'].queryset = ClassVoltage.objects.filter(pk__gt=2)
        return render(request, 'tula_net/form_add_line.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        bound_form = Line1Form(request.POST)
        if bound_form.is_valid():
            new_line = bound_form.save()
            return redirect(new_line)
        return render(request, 'tula_net/form_add_line.html', context={'form': bound_form})


class UpdLineView(UpdateView):
    model = Line
    form_class = Line1Form
    template_name = 'tula_net/form_add_line.html'


class LineDeleteView(DeleteObjectMixin, View):
    """ удаление ВЛ"""
    model = Line
    target_reverse = 'main'



class MyLogin(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main')
        form = UserAutForm()
        return render(request, 'login.html', {'form': form, 'my_login': 'Вход', })

    def post(self, request):
        form = UserAutForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
        return render(request, 'login.html', context={'form': form, })