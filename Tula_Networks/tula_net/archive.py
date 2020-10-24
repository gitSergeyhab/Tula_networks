# class PsList(ListView):
#     """ все ПС """
#     model = Substation
#     context_object_name = 'substations'
#     template_name = 'tula_net/substations.html'
#     extra_context = title1
#     """ context['groups'] - меню в верху страницы с названиями групп ПС
#     ['flag_group'] - для того чтобы не выводить названия групп, если группа уже выбрана и убрать поле поиска """
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['context_menu'] = context_menu
#         context['groups'] = Group.objects.all()
#         context['voltages'] = [35, 110, 220]
#         return context


# class AllFeedersView(ListView):
# #     """ все фидера вообще и сразу """
# #     model = Feeder
# #     template_name = 'tula_net/feeders.html'
# #     context_object_name = 'feeders'
# #
# #     def get_context_data(self, *, object_list=None, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context['context_menu'] = context_menu
# #         return context

# class AddFeederFromPSView1(View):
#     """ добавление фидера c ПС !!! и оно работает !!!"""
#
#     def get(self, request, *args, **kwargs):
#         form = FeederFormAdd()
#         form.fields["substation"].queryset = Substation.objects.filter(pk=self.kwargs['pk'])
#         form.fields["section"].queryset = Section.objects.filter(substation__pk=self.kwargs['pk'])
#         return render(request, 'tula_net/form_add_feeder.html', context={'form': form})
#
#     def post(self, request, *args, **kwargs):
#         bound_form = FeederFormAdd(request.POST)
#         if bound_form.is_valid():
#             new_feeder = bound_form.save()
#             return redirect(new_feeder)
#         return render(request, 'tula_net/form_add_feeder.html', context={'form': bound_form})





# class FeederFormAdd(BaseCrispyForms, forms.ModelForm):
#     """ для того чтобы прописать empty_label=None """
#     substation = forms.ModelChoiceField(label='ПС',empty_label=None, queryset=Substation.objects.all())
#     section = forms.ModelChoiceField(label='Секция',empty_label=None, queryset=Section.objects.all())
#     """ для того чтобы уменьшить поле описания """
#     description = forms.CharField(label='Примечание',required=False, widget=forms.Textarea(attrs={"rows": 3, }))
#
#     class Meta:
#         model = Feeder
#         fields = '__all__'