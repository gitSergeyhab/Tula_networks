from django.contrib import admin

# Register your models here.
from .models import Substation, Section, Feeder, Subscriber, Person, Phone, Group, Res, ClassVoltage, TransmissionLine,\
    Region, GroupLine


# автокомплит не работает:
# from dal import autocomplete
# from django import forms
# from .forms import FeederFormAdd


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
    list_display = ['pk', 'short_name', 'name', 'ours', 'year_update']
    list_display_links = ['short_name', 'name']
    search_fields = ['short_name', 'name']
    list_filter = ['ours']


admin.site.register(Subscriber, SubscriberAdmin)


class PersonAdnin(admin.ModelAdmin):
    list_display = ['priority', 'name', 'subscriber', 'position']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['subscriber']


admin.site.register(Person, PersonAdnin)


class FeederAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'substation', 'section', 'subscriber', 'attention', 'number_tp', 'in_reserve']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['substation', 'attention']


admin.site.register(Feeder, FeederAdmin)


class PhoneAdmin(admin.ModelAdmin):
    list_display = ['pk', 'number', 'search_number', 'subscriber', 'person', 'mail', 'priority']
    list_display_links = ['number']
    search_fields = ['number']
    list_filter = ['priority', 'subscriber', ]


admin.site.register(Phone, PhoneAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'ours']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name', ]


class ResAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'name']
    list_display_links = ['name', 'short_name', ]
    search_fields = ['name']
    list_filter = ['name', ]


class ClassVoltageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'class_voltage']
    list_display_links = ['pk', 'class_voltage']


class RegionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']


class LineAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'short_name', 'voltage', 'kvl', 'subscriber']
    list_display_links = ['name']
    search_fields = ['name', 'short_name', ]
    list_filter = [ 'management', 'voltage']

class GroupLineAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'ours']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name', ]


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupLine, GroupLineAdmin)
admin.site.register(Res, ResAdmin)
admin.site.register(ClassVoltage, ClassVoltageAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(TransmissionLine, LineAdmin)
