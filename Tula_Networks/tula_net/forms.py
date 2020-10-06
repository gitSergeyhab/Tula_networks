from django import forms
from django.forms import TextInput

from .models import Feeder, Subscriber
from dal import autocomplete

#
class FeederForm(forms.ModelForm):
    class Meta:
        model = Feeder
        fields = '__all__'
        # fields = ('name', 'subscriber', 'length', 'number_tp', 'population', 'social', 'res', 'attention', 'reliability_category', 'description',)
        widgets = {
            'subscriber': autocomplete.ModelSelect2(url='subscriber_autocomplete'),
            'substation': autocomplete.ModelSelect2(url='substation_autocomplete')
        }


# class FeederForm(forms.ModelForm):
#     subscriber = forms.ModelChoiceField(
#         queryset=Subscriber.objects.all(),
#         widget=autocomplete.ModelSelect2(url='subscriber_autocomplete')
#     )
#     class Meta:
#         model = Feeder
#         fields = '__all__'

