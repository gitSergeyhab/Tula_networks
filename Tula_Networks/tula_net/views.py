from django.shortcuts import render
from django.views import View

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Substation, Subscriber, Section, Person, Phone, Feeder, Group, Res

title = 'Тульские Сети'
context1 = {'substations': 'Подстанции',  'sections': 'Секции', }

# context1 = {'substations': 'Подстанции', 'subscribers': 'Абоненты', 'feeders': 'Присоединения',
#             'persons': 'Ответственные лица', 'sections': 'Секции', 'phones': 'Телефоны'}

title1 = {'title': title}
context2 = {'context1': context1, 'title': title}


class Main(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tula_net/index.html', context=context2)


class PsList(ListView):
    model = Substation
    context_object_name = 'substations'
    template_name = 'tula_net/listPS.html'
    extra_context = title1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context1'] = context1
        context['groups'] = Group.objects.all()
        context['flag_group'] = 1
        return context


class GroupPS(ListView):
    context_object_name = 'substations'
    template_name = 'tula_net/listPS.html'

    def get_queryset(self):
        return Substation.objects.filter(group__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['context1'] = context1
        return context


class ResPS(ListView):
    pass


class OnePS(DetailView):
    model = Substation
    template_name = 'tula_net/onePS.html'
    context_object_name = 'ps'


class SectionList(ListView):
    model = Section
    template_name = 'tula_net/section.html'
    context_object_name = 'sections'




class AllFeeders(ListView):
    model = Feeder
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'


# одна секция - лист фидеров
class OneSection(ListView):
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'

    def get_queryset(self):
        return Feeder.objects.filter(section__pk=self.kwargs['pk'])


class OneSubstation(ListView):
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'

    def get_queryset(self):
        return Feeder.objects.filter(substation__pk=self.kwargs['pk'])


class SectionPS(ListView):
    template_name = 'tula_net/section.html'
    context_object_name = 'sections'

    def get_queryset(self):
        return Section.objects.filter(substation__pk=self.kwargs['pk'])
