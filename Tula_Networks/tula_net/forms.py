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
class FeederFormAdd(BaseCrispyForms, forms.ModelForm):
    """ для того чтобы прописать empty_label=None """
    substation = forms.ModelChoiceField(empty_label=None, queryset=Substation.objects.all())
    section = forms.ModelChoiceField(empty_label=None, queryset=Section.objects.all())

    class Meta:
        model = Feeder
        fields = '__all__'


## ____________________ изменение Фидера  ______________________
class FeederFormUpd(BaseCrispyForms, forms.ModelForm):
    class Meta:
        model = Feeder
        fields = ['name', 'section', 'subscriber', 'number_tp', 'population', 'social', 'length',
                  'attention', 'res', 'reliability_category', 'in_reserve', 'description']



# __________________ форма добавления телефона для организации _______________________
class PhoneSubscriberFormAdd(PhoneFormAddMixin, forms.ModelForm):
    """ для того чтобы прописать empty_label=None """
    subscriber = forms.ModelChoiceField(empty_label=None, queryset=Subscriber.objects.all())

    class Meta:
        model = Phone
        fields = ('number', 'mail', 'subscriber', 'priority', 'description', 'search_number')


# __________________ форма добавления телефона для человека _______________________
class PhonePersonFormAdd(PhoneFormAddMixin, forms.ModelForm):
    person = forms.ModelChoiceField(empty_label=None, queryset=Person.objects.all())

    class Meta:
        model = Phone
        fields = ('number', 'mail', 'person', 'priority', 'description', 'search_number')


# __________________ форма добавления телефона для ПС _______________________
class PhonePSFormAdd(PhoneFormAddMixin, forms.ModelForm):
    substation = forms.ModelChoiceField(empty_label=None, queryset=Substation.objects.all())

    class Meta:
        model = Phone
        fields = ('number', 'mail', 'substation', 'priority', 'description', 'search_number')


# __________________ редактирование телефона  _______________________
class PhoneFormUpd(PhoneFormAddMixin, forms.ModelForm):
    class Meta:
        model = Phone
        fields = ('number', 'mail', 'person', 'subscriber', 'substation', 'priority', 'description', 'search_number')