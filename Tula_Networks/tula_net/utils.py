from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Feeder, Subscriber, Substation, Section, Phone, Person
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import re


# ____ шаблон для форм ___
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
