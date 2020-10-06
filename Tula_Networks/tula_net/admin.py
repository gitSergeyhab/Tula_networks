from django.contrib import admin

# Register your models here.
from .models import Substation, Section, Feeder, Subscriber, Person, Phone, Group, Res


from dal import autocomplete
from django import forms
from .forms import FeederForm





class SubstationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'number', 'name', 'voltage_h', 'voltage_m', 'voltage_l', 'group', 'alien']
    list_display_links = ['number', 'name']
    search_fields = ['number', 'name']
    list_filter = ['voltage_h', 'voltage_m', 'voltage_l', 'group', 'alien']


admin.site.register(Substation, SubstationAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display = ['substation', 'name', 'voltage']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['voltage', 'substation']


admin.site.register(Section, SectionAdmin)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['pk', 'short_name', 'name', 'ours']
    list_display_links = ['short_name', 'name']
    search_fields = ['short_name', 'name']
    list_filter = ['ours']



admin.site.register(Subscriber, SubscriberAdmin)

'''
class Person(models.Model):
    name = models.CharField(max_length=64, verbose_name='ФИО')
    priority = models.PositiveSmallIntegerField(blank=True, verbose_name='приоритет')
    description = models.TextField(verbose_name='Описение', blank=True)

'''


class PersonAdnin(admin.ModelAdmin):
    # form =
    list_display = ['priority', 'name', 'subscriber', 'position']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['subscriber']




admin.site.register(Person, PersonAdnin)


class FeederAdmin(admin.ModelAdmin):
    form = FeederForm
    # list_display = ['name', 'substation', 'section', 'subscriber', 'res', 'attention', 'number_tp']
    # list_display_links = ['name']
    # search_fields = ['name']
    # list_filter = ['substation', 'res', 'attention']


admin.site.register(Feeder, FeederAdmin)


class PhoneAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'person', 'number', 'mail', 'priority']
    list_display_links = ['number']
    search_fields = ['number']
    list_filter = ['priority', 'subscriber', ]


admin.site.register(Phone, PhoneAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ['pk','name']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name', ]


class ResAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'name']
    list_display_links = ['name', 'short_name', ]
    search_fields = ['name']
    list_filter = ['name', ]

admin.site.register(Group, GroupAdmin)
admin.site.register(Res, ResAdmin)


'''
class Group(models.Model):
    name = models.CharField(max_length=32, verbose_name='Группа', unique=True)
    location = models.TextField(verbose_name='Расположение', blank=True)
    description = models.TextField(verbose_name='Описение', blank=True)

    def get_absolute_url(self):
        return reverse('groups', kwargs={'pk': self.pk})


class Res(models.Model):
    name = models.CharField(max_length=32, verbose_name='РЭС', unique=True)
    location = models.TextField(verbose_name='Расположение', blank=True)
    description = models.TextField(verbose_name='Описение', blank=True))


'''
