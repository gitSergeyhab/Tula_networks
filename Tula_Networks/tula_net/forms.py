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

    class Meta:
        model = Feeder
        fields = '__all__'


class FeederFormUpd(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'сохранить'))

    class Meta:
        model = Feeder
        fields = ['name', 'section', 'subscriber', 'number_tp', 'population', 'social', 'length',
                  'attention', 'res', 'reliability_category', 'in_reserve', 'description']
        """
            name = models.CharField(max_length=32, verbose_name='Название фидера')
    substation = models.ForeignKey(Substation, related_name='feeders', on_delete=models.CASCADE, verbose_name='ПС')
    section = models.ForeignKey(Section, related_name='feeders', on_delete=models.CASCADE, verbose_name='СкШ')
    subscriber = models.ForeignKey(Subscriber, related_name='feeders', on_delete=models.SET_NULL,
                                   verbose_name='абонент', blank=True, null=True)
    length = models.PositiveSmallIntegerField(blank=True, verbose_name='Протяженность', null=True)
    number_tp = models.PositiveSmallIntegerField(blank=True, verbose_name='Количество ТП', null=True)
    population = models.PositiveSmallIntegerField(blank=True, verbose_name='Население', null=True)
    social = models.PositiveSmallIntegerField(blank=True, verbose_name='Социалка', null=True)
    res = models.ForeignKey(Res, related_name='feeders', verbose_name='РЭС или еще кто',
                            on_delete=models.SET_NULL, blank=True, null=True)
    attention = models.BooleanField(verbose_name='!!!')
    reliability_category = models.PositiveSmallIntegerField(blank=True, verbose_name='категория надежности', null=True)
    description = models.TextField(verbose_name='Описение', blank=True)
        
        """

# class FeederForm(forms.ModelForm):
#     sku = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     subscriber = forms.ModelChoiceField(
#         queryset=Subscriber.objects.all(),
#         widget=autocomplete.ModelSelect2(url='subscriber_autocomplete')
#     )
#     class Meta:
#         model = Feeder
#         fields = '__all__'
