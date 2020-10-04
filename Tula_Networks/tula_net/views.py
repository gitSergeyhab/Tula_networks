from django.shortcuts import render
from django.views import View

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Substation, Subscriber, Section, Person, Phone, Feeder, Group, Res
from .data import colors
title = 'Тульские Сети'
context_menu = {'substations': 'Подстанции', 'subscribers': 'Абоненты', }

# context_menu = {'substations': 'Подстанции', 'subscribers': 'Абоненты', 'feeders': 'Присоединения',
#             'persons': 'Ответственные лица', 'sections': 'Секции', 'phones': 'Телефоны'}

title1 = {'title': title}
context2 = {'context_menu': context_menu, 'title': title}


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
        context['context_menu'] = context_menu
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
        return context


class SubstationsBySubscriber(ListView):
    context_object_name = 'substations'
    template_name = 'tula_net/substations_by_ss.html'

    def get_queryset(self):
        return Substation.objects.filter(feeders__subscriber__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_subscriber'] = Subscriber.objects.get(pk=self.kwargs['pk'])
        context['context_menu'] = context_menu
        return context


class ResPS(ListView):
    pass


class OnePS(DetailView):
    model = Substation
    template_name = 'tula_net/onePS.html'
    context_object_name = 'ps'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


class SectionList(ListView):
    model = Section
    template_name = 'tula_net/section.html'
    context_object_name = 'sections'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


class AllFeeders(ListView):
    model = Feeder
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


# одна секция - лист фидеров
class OneSection(ListView):
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'

    def get_queryset(self):
        return Feeder.objects.filter(section__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


class OneSubstation(ListView):
    template_name = 'tula_net/feeders.html'
    context_object_name = 'feeders'

    def get_queryset(self):
        return Feeder.objects.filter(substation__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


class SectionPS(ListView):
    template_name = 'tula_net/section.html'
    context_object_name = 'sections'

    def get_queryset(self):
        return Section.objects.filter(substation__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_substation'] = Substation.objects.get(pk=self.kwargs['pk'])
        context['context_menu'] = context_menu
        return context


class OneSubscriber(DetailView):
    model = Subscriber
    template_name = 'tula_net/one_subscriber.html'
    context_object_name = 'subscriber'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context_menu'] = context_menu
        return context


class SubscriberList(ListView):
    model = Subscriber
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers_all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubscribersBySection(ListView):
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers.html'

    def get_queryset(self):
        return Subscriber.objects.filter(feeders__section__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_section'] = Section.objects.get(pk=self.kwargs['pk'])
        return context


class SubscribersByPS(ListView):
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers.html'

    def get_queryset(self):
        return Subscriber.objects.filter(feeders__substation__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_substation'] = Substation.objects.get(pk=self.kwargs['pk'])
        return context


class SearcherSubscribers(ListView):
    context_object_name = 'subscribers'
    template_name = 'tula_net/subscribers_all.html'

    def get_queryset(self):
        return Subscriber.objects.filter(name__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_search'] = self.request.GET.get('s')
        return context


class SearcherPS(ListView):
    context_object_name = 'substations'
    template_name = 'tula_net/listPS.html'

    def get_queryset(self):
        return Substation.objects.filter(name__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_search'] = self.request.GET.get('s')
        context['groups'] = Group.objects.all()

        context['flag_group'] = 1
        return context

