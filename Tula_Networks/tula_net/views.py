from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import FeederAddFromPSForm, FeederFormUpd, PhoneSubscriberFormAdd, PhonePersonFormAdd, PhoneFormUpd, \
    PhonePSFormAdd, SubscriberFormAdd, PersonFormAdd, SubstationFormUpd, FeederAddFromSubscriberForm, SectionAddForm

from .models import Substation, Subscriber, Section, Person, Phone, Feeder, Group, Res
from dal import autocomplete

from .utils import AddPhoneViewMixin, DeleteObjectMixin, SubstationsViewMixin, FeedersViewMixin, AddFeederMixin

from .data import context_menu


class MainView(View):
    """ главная """
    def get(self, request, *args, **kwargs):
        return render(request, 'tula_net/index.html', context={'context_menu': context_menu})


class PsListView (SubstationsViewMixin, ListView):
    """ вьюха для всех ПС """
    paginate_by = 24


class GroupPSView(SubstationsViewMixin, ListView):
    """ вьюха для ПС с разбивкой по группе """
    flag = 'flag_group'

    def get_queryset(self):
        return Substation.objects.filter(group__pk=self.kwargs['pk'])


class VoltPSView1(SubstationsViewMixin, ListView):
    """ вьюха для ПС с разбивкой по напряжению """
    flag = 'flag_voltages'

    def get_queryset(self):
        return Substation.objects.filter(voltage_h=self.kwargs['pk'])


class VoltPSView(SubstationsViewMixin, ListView):
    """ вьюха для ПС с разбивкой по напряжению """
    flag = 'flag_voltages'

    def get_queryset(self):
        return Substation.objects.filter(voltage_h__class_voltage=self.kwargs['pk'])



class SubstationsBySubscriberView(ListView):
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


class OnePSView(DetailView):
    """ карточка одной пс """
    model = Substation
    template_name = 'tula_net/onePS.html'
    context_object_name = 'ps'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


class SectionListView(ListView):
    """ все секции с фидерами - бесполезная) """
    model = Section
    template_name = 'tula_net/section.html'
    context_object_name = 'sections'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


# ____________фидера_____________
class OneFeedersView(DetailView):
    model = Feeder
    template_name = 'tula_net/feeder.html'
    context_object_name = 'feeder'


class AllFeedersView(FeedersViewMixin, ListView):
    """ все фидера вообще и сразу """
    model = Feeder


class SectionView(DetailView):
    model = Section
    context_object_name = 'section'
    template_name = 'tula_net/one_section.html'



class OneSectionView(FeedersViewMixin, ListView):
    """ одна секция - лист фидеров """
    second_model = Section
    the_context = 'the_section'

    def get_queryset(self):
        return Feeder.objects.filter(section__pk=self.kwargs['pk'])


class OneSubstationView(FeedersViewMixin, ListView):
    """ одна ПС - лист фидеров """
    second_model = Substation
    the_context = 'the_substation'

    def get_queryset(self):
        return Feeder.objects.filter(substation__pk=self.kwargs['pk'])



class SectionPSView(ListView):
    template_name = 'tula_net/section.html'
    context_object_name = 'sections'

    def get_queryset(self):
        return Section.objects.filter(substation__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_substation'] = Substation.objects.get(pk=self.kwargs['pk'])
        context['context_menu'] = context_menu
        return context


class OneSubscriberView(DetailView):
    model = Subscriber
    template_name = 'tula_net/one_subscriber.html'
    context_object_name = 'subscriber'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


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
        return Subscriber.objects.filter(feeders__section__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_section'] = Section.objects.get(pk=self.kwargs['pk'])
        return context


class SubscribersByPSView(ListView):
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
class PersonListView(ListView):
    """ список всех людей """
    model = Person
    template_name = 'tula_net/persons.html'
    context_object_name = 'persons'


class OnePersonView(DetailView):
    """ один человек """
    model = Person
    template_name = 'tula_net/one_person.html'
    context_object_name = 'person'


# ____________ телефоны _______________
class PhoneListView(ListView):
    model = Phone
    template_name = 'tula_net/phones.html'
    context_object_name = 'phones'


class OnePhoneView(DetailView):
    """ один телефон """
    model = Phone
    template_name = 'tula_net/one_phone.html'
    context_object_name = 'phone'


# __________________ Поиски ____________________
class SearcherSubscribersView(ListView):
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


class SearcherPSView(ListView):
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
        context['voltages'] = [35, 110, 220]
        return context


class SearcherPersonsView(ListView):
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


class SearcherPhonesView(ListView):
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
        form.fields['section'].queryset = Section.objects.filter(substation__feeders__pk=pk)
        form.fields['substation'].queryset = Substation.objects.filter(feeders__pk=pk)
        return render(request, 'tula_net/form_add_feeder.html', context={'form': form})

    def post(self,request, pk):
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


class UpdPhoneView(UpdateView):
    """ изменение телефона"""
    form_class = PhoneFormUpd
    model = Phone
    template_name = 'tula_net/form_add_phone.html'


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








# ___________________
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
# ________________________
