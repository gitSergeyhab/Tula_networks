from django import forms
from django.forms import TextInput, SelectDateWidget

from .models import Feeder, Subscriber, Substation, Section, Phone, Person
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
    substation = forms.ModelChoiceField(label='ПС',empty_label=None, queryset=Substation.objects.all())
    section = forms.ModelChoiceField(label='Секция',empty_label=None, queryset=Section.objects.all())


class FeederAddFromSubscriberForm(FeederBaseForm):
    subscriber = forms.ModelChoiceField(label='Организация', empty_label=None, queryset=Subscriber.objects.all())

## ____________________ изменение Фидера  ______________________
class FeederFormUpd(BaseCrispyForms, forms.ModelForm):
    description = forms.CharField(label='Примечание',required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Feeder
        fields = ['name', 'section', 'subscriber', 'number_tp', 'population', 'social', 'length',
                  'attention', 'res', 'reliability_category', 'in_reserve', 'description']


# __________________ форма добавления телефона для организации _______________________
class PhoneSubscriberFormAdd(PhoneFormAddMixin, forms.ModelForm):
    """ для того чтобы прописать empty_label=None """
    subscriber = forms.ModelChoiceField(label='Организация',empty_label=None, queryset=Subscriber.objects.all())

    description = forms.CharField(label='Примечание',required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Phone
        fields = ('number', 'mail', 'subscriber', 'priority', 'description', 'search_number')


# __________________ форма добавления телефона для человека _______________________
class PhonePersonFormAdd(PhoneFormAddMixin, forms.ModelForm):
    person = forms.ModelChoiceField(label='Кто',empty_label=None, queryset=Person.objects.all())
    description = forms.CharField(label='Примечание',required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Phone
        fields = ('number', 'mail', 'person', 'priority', 'description', 'search_number')


# __________________ форма добавления телефона для ПС _______________________
class PhonePSFormAdd(PhoneFormAddMixin, forms.ModelForm):
    substation = forms.ModelChoiceField(label='ПС', empty_label=None, queryset=Substation.objects.all())
    description = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Phone
        fields = ('number', 'mail', 'substation', 'priority', 'description', 'search_number')


# __________________ редактирование телефона  _______________________
class PhoneFormUpd(PhoneFormAddMixin, forms.ModelForm):
    description = forms.CharField(label='Примечание', required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Phone
        fields = ('number', 'mail', 'person', 'subscriber', 'substation', 'priority', 'description', 'search_number')


# ____________________  Организации  ______________________
class SubscriberFormAdd(BaseCrispyForms, forms.ModelForm):
    description = forms.CharField(label='Описание',required=False, widget=forms.Textarea(attrs={"rows": 3, }))

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
    description = forms.CharField(label='Описание',required=False, widget=forms.Textarea(attrs={"rows": 3, }))

    class Meta:
        model = Section
        fields = '__all__'
