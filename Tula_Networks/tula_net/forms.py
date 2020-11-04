from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import TextInput, SelectDateWidget

from .models import Feeder, Subscriber, Substation, Section, Phone, Person, Line, Feeder_characteristic
from dal import autocomplete

from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import re

from .utils import PhoneFormAddMixin, BaseCrispyForms


#
# ____________________  Фидеры  ______________________
## ____________________ добавление Фидера  ______________________

class FeederBaseForm(BaseCrispyForms, forms.ModelForm):
    """ базовая форма для добавления фидера """
    description = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Feeder
        fields = '__all__'


class FeederAddFromPSForm(FeederBaseForm):
    """ базовая форма для добавления фидера с ПС """

    """ для того чтобы прописать empty_label=None """
    substation = forms.ModelChoiceField(label='ПС', empty_label=None, queryset=Substation.objects.all())
    section = forms.ModelChoiceField(label='Секция', empty_label=None, queryset=Section.objects.all())


class FeederAddFromSubscriberForm(FeederBaseForm):
    subscriber = forms.ModelChoiceField(label='Организация', empty_label=None, queryset=Subscriber.objects.all())


## ____________________ изменение Фидера  ______________________
class FeederFormUpd(BaseCrispyForms, forms.ModelForm):
    description = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Feeder
        # fields = '__all__'
        fields = ['name', 'substation', 'section', 'subscriber', 'in_reserve', 'attention', 'description']


class FeederCharForm(BaseCrispyForms, forms.ModelForm):

    class Meta:
        model = Feeder_characteristic
        fields = '__all__'



# __________________ форма добавления телефона для организации _______________________
class PhoneSubscriberFormAdd(PhoneFormAddMixin, forms.ModelForm):
    """ для того чтобы прописать empty_label=None """
    subscriber = forms.ModelChoiceField(label='Организация', empty_label=None, queryset=Subscriber.objects.all())

    description = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Phone
        fields = ('number',  'subscriber', 'priority', 'description', 'search_number')


# __________________ форма добавления телефона для человека _______________________
class PhonePersonFormAdd(PhoneFormAddMixin, forms.ModelForm):
    person = forms.ModelChoiceField(label='Кто', empty_label=None, queryset=Person.objects.all())
    description = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Phone
        fields = ('number', 'person', 'priority', 'description', 'search_number')


# __________________ форма добавления телефона для ПС _______________________
class PhonePSFormAdd(PhoneFormAddMixin, forms.ModelForm):

    substation = forms.ModelChoiceField(label='ПС', empty_label=None, queryset=Substation.objects.all())
    description = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Phone
        fields = ('number', 'substation', 'priority', 'description', 'search_number')


# __________________ редактирование телефона  _______________________
class PhoneFormUpd(PhoneFormAddMixin, forms.ModelForm):
    description = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Phone
        fields = ('number', 'person', 'subscriber', 'substation', 'priority', 'description', 'search_number')


# ____________________  Организации  ______________________
class SubscriberFormAdd(BaseCrispyForms, forms.ModelForm):
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Subscriber
        fields = '__all__'


class PersonFormAdd(BaseCrispyForms, forms.ModelForm):
    subscriber = forms.ModelChoiceField(label='Организация', empty_label=None, queryset=Subscriber.objects.all())
    description = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Person
        fields = '__all__'


class SubstationFormUpd(BaseCrispyForms, forms.ModelForm):
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))
    location = forms.CharField(label='Расположение', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Substation
        fields = '__all__'


class SectionAddForm(BaseCrispyForms, forms.ModelForm):
    substation = forms.ModelChoiceField(label='ПС', empty_label=None, queryset=Substation.objects.all())
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Section
        fields = '__all__'




class Line1Form(BaseCrispyForms, forms.ModelForm):
    # description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={"rows": 1, }))
    class Meta:
        model = Line
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'management': forms.Select(attrs={'class': 'form-control'}),
            'maintenance': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'subscriber': forms.Select(attrs={'class': 'form-control'}),
            'voltage': forms.Select(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'ps_p1': forms.NumberInput(attrs={'class': 'form-control'}),
            'ps_p2': forms.NumberInput(attrs={'class': 'form-control'}),
            'sec_p1': forms.NumberInput(attrs={'class': 'form-control'}),
            'sec_p2': forms.NumberInput(attrs={'class': 'form-control'}),
            'ps_m1': forms.NumberInput(attrs={'class': 'form-control'}),
            'ps_m2': forms.NumberInput(attrs={'class': 'form-control'}),
            'ps_m3': forms.NumberInput(attrs={'class': 'form-control'}),
            'ps_m4': forms.NumberInput(attrs={'class': 'form-control'}),
            'sec_m1': forms.NumberInput(attrs={'class': 'form-control'}),
            'sec_m2': forms.NumberInput(attrs={'class': 'form-control'}),
            'sec_m3': forms.NumberInput(attrs={'class': 'form-control'}),
            'sec_m4': forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_columns': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # 'kvl': forms.BooleanField(),
        }


class UserAutForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
