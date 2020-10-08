from django import forms
from .models import Feeder, Subscriber, Substation, Section, Phone, Person
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import re




class PhoneFormAddMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'сохранить'))

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-7'

    def clean_search_number(self):
        raw_number = self.cleaned_data['number']
        for i in raw_number:
            if i.isalpha():
                raise ValueError('хм, а у Вас в номере буквы, например...', i)
        search_number = ''.join([sign for sign in raw_number if sign.isdigit()])
        return search_number