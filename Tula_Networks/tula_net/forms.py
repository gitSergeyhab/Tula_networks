from django import forms
from django.forms import TextInput, SelectDateWidget

from .models import Feeder, Subscriber, Substation, Section
from dal import autocomplete

from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


#

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
        """

        """
