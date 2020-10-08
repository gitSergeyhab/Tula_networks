from django import forms
from django.forms import TextInput, SelectDateWidget

from .models import Feeder, Subscriber, Substation, Section, Phone, Person
from dal import autocomplete

from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import re


#
# ____________________  Фидеры  ______________________
## ____________________ добавление Фидера  ______________________
class FeederFormAdd(forms.ModelForm):
    """ для того чтобы прописать empty_label=None """
    substation = forms.ModelChoiceField(empty_label=None, queryset=Substation.objects.all())
    section = forms.ModelChoiceField(empty_label=None, queryset=Section.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'сохранить'))

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-7'

    class Meta:
        model = Feeder
        fields = '__all__'


## ____________________ изменение Фидера  ______________________
class FeederFormUpd(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'сохранить изменения'))

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-7'

    class Meta:
        model = Feeder
        fields = ['name', 'section', 'subscriber', 'number_tp', 'population', 'social', 'length',
                  'attention', 'res', 'reliability_category', 'in_reserve', 'description']


# ________________ телефоны ___________________
## ___________ добавление телефона  ___________
class PhoneSFormAdd(forms.ModelForm):
    """ для того чтобы прописать empty_label=None """

    subscriber = forms.ModelChoiceField(empty_label=None, queryset=Subscriber.objects.all())
    # person = forms.ModelChoiceField(empty_label=None, queryset=Person.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'сохранить'))

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-7'

    class Meta:
        model = Phone
        fields = ('number', 'mail', 'subscriber', 'substation', 'priority', 'description', 'search_number')

    def clean_search_number(self):
        raw_number = self.cleaned_data['number']
        if re.match(r'[A-Za-zА-Яа-я]', raw_number):
            raise ValueError('хм, а у Вас в номере буквы...')
        search_number = ''.join([sign for sign in raw_number if sign.isdigit()])
        return search_number

# class PhoneSFormUpd
class PhonePFormAdd(forms.ModelForm):
    """ для того чтобы прописать empty_label=None """

    # subscriber = forms.ModelChoiceField(empty_label=None, queryset=Subscriber.objects.all())
    person = forms.ModelChoiceField(empty_label=None, queryset=Person.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'сохранить'))

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-7'

    class Meta:
        model = Phone
        fields = ('number', 'mail',  'person', 'substation','priority', 'description', 'search_number')

    def clean_search_number(self):
        raw_number = self.cleaned_data['number']
        if re.match(r'[A-Za-zА-Яа-я]', raw_number):
            raise ValueError('хм, а у Вас в номере буквы...')
        search_number = ''.join([sign for sign in raw_number if sign.isdigit()])
        return search_number


class PhonePSFormAdd(forms.ModelForm):
    """ для того чтобы прописать empty_label=None """

    substation = forms.ModelChoiceField(empty_label=None, queryset=Substation.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'сохранить'))

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-7'

    class Meta:
        model = Phone
        fields = ('number', 'mail', 'substation','priority', 'description', 'search_number')

    def clean_search_number(self):
        raw_number = self.cleaned_data['number']
        if re.match(r'[A-Za-zА-Яа-я]', raw_number):
            raise ValueError('хм, а у Вас в номере буквы...')
        search_number = ''.join([sign for sign in raw_number if sign.isdigit()])
        return search_number


class PhoneFormUpd(forms.ModelForm):
    """ для того чтобы прописать empty_label=None """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'сохранить'))

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-7'

    class Meta:
        model = Phone
        fields = ('number', 'mail',  'person' ,'subscriber', 'substation','priority', 'description', 'search_number')

    def clean_search_number(self):
        raw_number = self.cleaned_data['number']
        if re.match(r'[A-Za-zА-Яа-я]', raw_number):
            raise ValueError('хм, а у Вас в номере буквы...')
        search_number = ''.join([sign for sign in raw_number if sign.isdigit()])
        return search_number