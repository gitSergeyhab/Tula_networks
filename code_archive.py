"""
# ___________ добавление телефона  ___________
class PhoneSFormAdd(forms.ModelForm):
   ''' для того чтобы прописать empty_label=None '''

    subscriber = forms.ModelChoiceField(empty_label=None, queryset=Subscriber.objects.all())
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
        for i in raw_number:
            if i.isalpha():
                raise ValueError('хм, а у Вас в номере буквы...', i)
        if re.match(r'[A-Za-zА-Яа-я]', raw_number):
            raise ValueError('хм, а у Вас в номере буквы...')
        search_number = ''.join([sign for sign in raw_number if sign.isdigit()])
        return search_number



## __________________ телефоны добавление телефона организации____________________

class AddSubscriberPhone1(View):

    def get(self, request, *args, **kwargs):
        form = PhoneSubscriberFormAdd()
        form.fields["subscriber"].queryset = Subscriber.objects.filter(pk=self.kwargs['pk'])
        return render(request, 'tula_net/form_add_phone.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        bound_form = PhoneSubscriberFormAdd(request.POST)
        if bound_form.is_valid():
            new_phone = bound_form.save()
            return redirect(new_phone)
        return render(request, 'tula_net/form_add_phone.html', context={'form': bound_form})




# _______________ удаление телефона _________________
class PhoneDelete(View):

    def get(self, request,*args, **kwargs):
        phone = Phone.objects.get(pk=self.kwargs['pk'])
        return render(request, 'tula_net/form_del_phone.html', context={'phone': phone})

    def post(self, request, *args, **kwargs):
        phone = Phone.objects.get(pk=self.kwargs['pk'])
        phone.delete()
        return redirect(reverse('phones'))


"""

"""
class PsList(ListView):

    model = Substation
    context_object_name = 'substations'
    template_name = 'tula_net/listPS.html'
    extra_context = title1


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        context['groups'] = Group.objects.all()
        context['voltages'] = [35, 110, 220]
        return context


"""

"""
Для первой модели ВЛ 
"""
# class SectionPSView(ListView):
#     template_name = 'tula_net/section.html'
#     context_object_name = 'sections'
#
#     def get_queryset(self):
#         return Section.objects.prefetch_related('feeders', 'lines', 'substation').select_related('voltage'). \
#             filter(substation__pk=self.kwargs['pk'])
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['the_substation'] = Substation.objects.get(pk=self.kwargs['pk'])
#         return context


# class LineForm(BaseCrispyForms, forms.ModelForm):
#     description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={"rows": 1, }))
#
#     class Meta:
#         model = TransmissionLine
#         fields = '__all__'


# class AddLineView(View):
#     """ добавление фидера c ПС !!! и оно работает !!!"""
#
#     def get(self, request, pk):
#         form = LineForm()
#         form.fields['section'].queryset = Section.objects.filter(voltage__pk=pk)
#         form.fields['voltage'].queryset = ClassVoltage.objects.filter(pk=pk)
#         form.fields['voltage'].initial = ClassVoltage.objects.get(pk=pk)
#         return render(request, 'tula_net/form_add_feeder.html', context={'form': form})
#
#     def post(self, request, *args, **kwargs):
#         bound_form = LineForm(request.POST)
#         if bound_form.is_valid():
#             new_line = bound_form.save()
#             return redirect(new_line)
#         return render(request, 'tula_net/form_add_feeder.html', context={'form': bound_form})


# class SectionView(DetailView):
#     context_object_name = 'section'
#     template_name = 'tula_net/one_section.html'
#
#     def get_queryset(self):
#         return Section.objects.prefetch_related('feeders', 'lines').all()




# class LinesViewMixin:
#     """ шаблон для  """
#     model = TransmissionLine
#     context_object_name = 'lines'
#     template_name = 'tula_net/lines.html'
#     menu = None  # добавление контехтного меню
#     flag = None  # добавление для отображения выборок ПС по группам и напряжению
#
#     def get_queryset(self):
#         return TransmissionLine.objects.select_related('management', 'voltage', 'group').all()
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['context_menu'] = self.menu
#         context['groups'] = GroupLine.objects.all()
#         context['voltages'] = ClassVoltage.objects.all()[1:3]
#         context['regions'] = Region.objects.filter(for_menu=True)
#         context[self.flag] = 1
#         return context





# class OneLineView(DetailView):
#     model = TransmissionLine
#     context_object_name = 'line'
#     template_name = 'tula_net/one_line.html'
#
#     def get_queryset(self):
#         return TransmissionLine.objects.prefetch_related('section', 'section__substation', 'maintenance'). \
#             select_related('management', 'group', 'voltage', 'subscriber')