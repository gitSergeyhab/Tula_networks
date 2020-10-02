from django.shortcuts import render
from django.views import View

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Substation, Subscriber, Section, Person, Phone, Feeder, Group, Res

title = 'Тульские Сети'
context1 = {'substations': 'Подстанции', 'subscribers': 'Абоненты', 'feeders': 'Присоединения',
            'persons': 'Ответственные лица', 'sections': 'Секции', 'phones': 'Телефоны'}

title1 = {'title': title}
context = {'context1': context1, 'title': title}


class Main(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tula_net/index.html', context=context)


class PsList(ListView):
    model = Substation
    context_object_name = 'substations'
    template_name = 'tula_net/listPS.html'
    extra_context = context




class PsGroupResHvolt:

    def get_groups(self):
        return Group.objects.all()

    def get_ress(self):
        return Res.objects.all()


class PsList1(PsGroupResHvolt, ListView):

    template_name = 'tula_net/listPS1.html'
    extra_context = context
    def get_queryset(self):
        return Substation.objects.filter(group__in=self.request.GET.getlist('group'))




class OnePS(DetailView):
    model = Substation
    template_name = 'tula_net/onePS.html'
    # context_object_name   на самом деле не требуется и не используется - используется   user  и  request.user
    context_object_name = 'substation'
    extra_context = context
