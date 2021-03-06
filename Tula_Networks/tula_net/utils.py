from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import re
# from .data import context_menu

# ____ шаблон для форм ___
from tula_net.models import Substation, Group, Feeder, Section, ClassVoltage, GroupLine, Region, Line


class BaseCrispyForms:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'сохранить изменения'))

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-7'


# ____ шаблон для форм телефонов ___
class PhoneFormAddMixin(BaseCrispyForms):

    def clean_search_number(self):
        raw_number = self.cleaned_data['number']
        # for i in raw_number:
        #     if i.isalpha():
        #         raise ValueError('хм, а у Вас в номере буквы, например...', i)
        search_number = ''.join([sign for sign in raw_number if sign.isdigit()])
        return search_number


class AddPhoneViewMixin:
    """ добавление телефона"""
    model = None
    form_x = None

    def get(self, request, *args, **kwargs):
        form = self.form_x()

        form.fields[self.model.__name__.lower()].queryset = self.model.objects.filter(pk=self.kwargs['pk'])
        form.fields['search_number'].widget = forms.HiddenInput()
        return render(request, 'tula_net/form_add_phone.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        bound_form = self.form_x(request.POST)
        if bound_form.is_valid():
            new_phone = bound_form.save()
            return redirect(new_phone)
        return render(request, 'tula_net/form_add_phone.html', context={'form': bound_form})


# _______________ удаление _________________
class DeleteObjectMixin:
    model = None
    target_reverse = None

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.get(pk=self.kwargs['pk'])
        return render(request, 'tula_net/form_delete_object.html', context={'obj': obj})

    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(pk=self.kwargs['pk'])
        obj.delete()
        return redirect(reverse(self.target_reverse))


# 345ms overall/46ms on queries/73 queries
# 72ms overall 5ms on queries 3 queries
class SubstationsViewMixin:
    """ шаблон для ПС """
    context_object_name = 'substations'
    template_name = 'tula_net/substations.html'
    menu = None  # добавление контехтного меню
    flag = None  # добавление для отображения выборок ПС по группам и напряжению

    def get_queryset(self):
        return Substation.objects.select_related('group', 'voltage_h', 'voltage_m', 'voltage_l').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['voltages'] = ClassVoltage.objects.all()[1:3]
        context[self.flag] = 1
        return context


class FeedersViewMixin:
    """ шаблон для фидеров """
    second_model = None  # модель в контекст для отображения конкретной секции ии ПС
    the_context = None  # см. предыд пункт
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'

    def get_queryset(self):
        return Feeder.objects.select_related('substation', 'section', 'subscriber', 'section__voltage').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.second_model:
            context[self.the_context] = self.second_model.objects.get(pk=self.kwargs['pk'])
        return context


def try_number_feeder(x):
    if x.isdigit():
        return int(x)
    return 0


class FeederFormMixin(BaseCrispyForms):

    def clean_search_number(self):
        raw_number = self.cleaned_data['name']
        try_number_name = ''.join([sign for sign in raw_number if sign.isdigit()])
        return try_number_name



class AddFeederMixin:
    """ шаблон для добавления фидера c ... """
    form_feeder = None
    first_model = None
    first_field = None
    second_field = None

    def get(self, request, pk):
        form = self.form_feeder()
        form.fields['try_number_name'].widget = forms.HiddenInput()
        form.fields[self.first_field].queryset = self.first_model.objects.filter(pk=pk)
        if self.second_field and self.second_field == 'section':
            form.fields[self.second_field].queryset = Section.objects.filter(substation__pk=pk,
                                                                             voltage__class_voltage__lte=10)
        if self.second_field and self.second_field == 'substation':
            form.fields[self.second_field].queryset = Substation.objects.filter(sections__pk=pk)
        return render(request, 'tula_net/form_add_feeder.html', context={'form': form})

    def post(self, request, pk):
        bound_form = self.form_feeder(request.POST)
        if bound_form.is_valid():
            new_feeder = bound_form.save(commit=False)
            try_num = bound_form.cleaned_data['name']
            new_feeder.try_number_name = try_number_feeder(try_num)
            new_feeder.save()
            return redirect(new_feeder)
        return render(request, 'tula_net/form_add_feeder.html', context={'form': bound_form})


def chang_search(obs):
    if '-' in obs:
        list_obs = obs.split('-')
        obs_n = ' - '.join([word.strip() for word in list_obs])
        print(obs_n)
        return obs_n
    return obs


def make_digits(num):
    return ''.join([n for n in num if n.isdigit()])


def try_int(num):
    try:
        x = int(num)
        return x
    except:
        return -1


class Lines1ViewMixin:
    """ шаблон для  """
    context_object_name = 'lines'
    template_name = 'tula_net/lines1.html'
    menu = None  # добавление контехтного меню
    flag = None  # добавление для отображения выборок ПС по группам и напряжению

    def get_queryset(self):
        return Line.objects.select_related('management', 'voltage', 'group')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['context_menu'] = self.menu
        context['groups'] = GroupLine.objects.all()
        context['voltages'] = ClassVoltage.objects.all()[1:3]
        context['regions'] = Region.objects.filter(for_menu=True)
        context[self.flag] = 1
        return context


class SearchMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['flag_search'] = self.request.GET.get('s')
        return context
