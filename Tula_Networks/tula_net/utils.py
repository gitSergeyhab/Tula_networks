from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import re
from .data import context_menu


# ____ шаблон для форм ___
from tula_net.models import Substation, Group, Feeder, Section


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
        for i in raw_number:
            if i.isalpha():
                raise ValueError('хм, а у Вас в номере буквы, например...', i)
        search_number = ''.join([sign for sign in raw_number if sign.isdigit()])
        return search_number


class AddPhoneViewMixin:
    """ добавление телефона"""
    model = None
    form_x = None

    def get(self, request, *args, **kwargs):
        form = self.form_x()

        form.fields[self.model.__name__.lower()].queryset = self.model.objects.filter(pk=self.kwargs['pk'])
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


class SubstationsViewMixin:
    """ шаблон для ПС """
    model = Substation
    context_object_name = 'substations'
    template_name = 'tula_net/listPS.html'
    menu = None # добавление контехтного меню
    flag = None # добавление для отображения выборок ПС по группам и напряжению

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = self.menu
        context['groups'] = Group.objects.all()
        context['voltages'] = [35, 110, 220]
        context[self.flag] = 1
        return context


class FeedersViewMixin:
    """ шаблон для фидеров """
    model = None
    second_model = None #  модель в контекст для оторажения конкретной секции ии ПС
    the_context = None # см. предыд пункт
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        if self.second_model:
            context[self.the_context] = self.second_model.objects.get(pk=self.kwargs['pk'])
        return context


class AddFeederMixin:
    """ шаблон для добавления фидера c ... """
    form_feeder = None
    first_model = None
    first_field = None
    second_field = None

    def get(self, request, pk):
        form = self.form_feeder()
        form.fields[self.first_field].queryset = self.first_model.objects.filter(pk=pk)
        if self.second_field and self.second_field == 'section':
            form.fields[self.second_field].queryset = Section.objects.filter(substation__pk=pk)
        return render(request, 'tula_net/form_add_feeder.html', context={'form': form})

    def post(self, request, pk):
        bound_form = self.form_feeder(request.POST)
        if bound_form.is_valid():
            new_feeder = bound_form.save()
            return redirect(new_feeder)
        return render(request, 'tula_net/form_add_feeder.html', context={'form': bound_form})

