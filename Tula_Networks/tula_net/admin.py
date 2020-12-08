from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

# Register your models here.
from .models import Substation, Section, Feeder, Subscriber, Person, Phone, Group, ClassVoltage,\
    Region, GroupLine, Line, Feeder_characteristic


class GroupResourse(resources.ModelResource):
    class Meta:
        model = Group


class GroupAdmin(ImportExportActionModelAdmin):
    resource_class = GroupResourse
    list_display = ['pk', 'name', 'ours']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name', ]


admin.site.register(Group, GroupAdmin)


class ClassVoltageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'class_voltage']
    list_display_links = ['pk', 'class_voltage']


admin.site.register(ClassVoltage, ClassVoltageAdmin)


class RegionResourse(resources.ModelResource):
    class Meta:
        model = Region


class RegionAdmin(ImportExportActionModelAdmin):
    resource_class = RegionResourse
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']


admin.site.register(Region, RegionAdmin)


class GroupLineAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'ours']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name', ]


admin.site.register(GroupLine, GroupLineAdmin)


class SubstationResourse(resources.ModelResource):
    voltage_h = fields.Field(attribute='voltage_h', widget=ForeignKeyWidget(ClassVoltage, 'class_voltage'))
    voltage_m = fields.Field(attribute='voltage_m', widget=ForeignKeyWidget(ClassVoltage, 'class_voltage'))
    voltage_l = fields.Field(attribute='voltage_l', widget=ForeignKeyWidget(ClassVoltage, 'class_voltage'))
    owner = fields.Field(attribute='owner', widget=ForeignKeyWidget(Subscriber, 'name'))
    group = fields.Field(attribute='group', widget=ForeignKeyWidget(Group, 'name'))
    region = fields.Field(attribute='region', widget=ForeignKeyWidget(Region, 'name'))

    class Meta:
        model = Substation
        export_order = ('id', 'number', 'name', 'voltage_h', 'voltage_m', 'voltage_l',
                        'alien', 'owner', 'group', 'location', 'region', 'description',)


class SubstationAdmin(ImportExportActionModelAdmin):
    resource_class = SubstationResourse
    list_display = ['pk', 'number', 'name', 'voltage_h', 'voltage_m', 'voltage_l', 'group', 'alien']
    list_display_links = ['number', 'name']
    search_fields = ['number', 'name']
    list_filter = ['voltage_h', 'voltage_m', 'voltage_l', 'group', 'alien']


admin.site.register(Substation, SubstationAdmin)


class SectionResourse(resources.ModelResource):
    substation = fields.Field(attribute='substation', widget=ForeignKeyWidget(Substation, 'name'))
    voltage = fields.Field(attribute='voltage', widget=ForeignKeyWidget(ClassVoltage, 'class_voltage'))

    class Meta:
        model = Section


class SectionAdmin(ImportExportActionModelAdmin):
    resource_class = SectionResourse
    list_display = ['substation', 'name', 'voltage']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['voltage', 'substation']

admin.site.register(Section, SectionAdmin)


class SubscriberResourse(resources.ModelResource):
    class Meta:
        model = Subscriber


class SubscriberAdmin(ImportExportActionModelAdmin):
    resource_class = SubscriberResourse
    list_display = ['pk', 'short_name', 'name', 'ours', 'year_update']
    list_display_links = ['short_name', 'name']
    search_fields = ['short_name', 'name']
    list_filter = ['ours']


admin.site.register(Subscriber, SubscriberAdmin)


class PersonResourse(resources.ModelResource):

    subscriber = fields.Field(attribute='subscriber', widget=ForeignKeyWidget(Subscriber, 'name'))

    class Meta:
        model = Person


class PersonAdnin(ImportExportActionModelAdmin):
    resource_class = PersonResourse
    list_display = ['priority', 'name', 'subscriber', 'position']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['subscriber']


admin.site.register(Person, PersonAdnin)


class FeederResourse(resources.ModelResource):
    substation = fields.Field(attribute='substation', widget=ForeignKeyWidget(Substation, 'name'))
    section = fields.Field(attribute='section', widget=ForeignKeyWidget(Section, 'name'))
    subscriber = fields.Field(attribute='subscriber', widget=ForeignKeyWidget(Subscriber, 'name'))
    region = fields.Field(attribute='region', widget=ForeignKeyWidget(Region, 'name'))

    class Meta:
        model = Feeder


class FeederAdmin(ImportExportActionModelAdmin):
    resource_class = FeederResourse
    list_display = ['pk', 'name', 'substation', 'section', 'subscriber', 'attention', 'in_reserve']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['substation', 'attention']


admin.site.register(Feeder, FeederAdmin)


class Feeder_characteristicResourse(resources.ModelResource):
    feeder = fields.Field(attribute='feeder', widget=ForeignKeyWidget(Feeder, ('name')))
    # лишнее поле!!!
    substation = fields.Field(attribute='feeder', widget=ForeignKeyWidget(Feeder, ('substation__name')))

    class Meta:
        model = Feeder_characteristic


class Feeder_characteristicAdmin(ImportExportActionModelAdmin):
    resource_class = Feeder_characteristicResourse
    list_display = ['feeder', 'length', 'population', 'points', 'checked']


admin.site.register(Feeder_characteristic, Feeder_characteristicAdmin)


class PhoneResourse(resources.ModelResource):
    subscriber = fields.Field(attribute='subscriber', widget=ForeignKeyWidget(Subscriber, 'name'))
    person = fields.Field(attribute='person', widget=ForeignKeyWidget(Person, 'name'))
    substation = fields.Field(attribute='substation', widget=ForeignKeyWidget(Substation, 'name'))

    class Meta:
        model = Phone


class PhoneAdmin(ImportExportActionModelAdmin):
    resource_class = PhoneResourse
    list_display = ['number', 'search_number', 'subscriber', 'person', 'substation']
    list_display_links = ['number']
    search_fields = ['number']
    list_filter = ['priority', 'subscriber', ]


admin.site.register(Phone, PhoneAdmin)


class LineResourse(resources.ModelResource):
    voltage = fields.Field(attribute='voltage', widget=ForeignKeyWidget(ClassVoltage, 'class_voltage'))
    management = fields.Field(attribute='management', widget=ForeignKeyWidget(Region, 'name'))
    subscriber = fields.Field(attribute='subscriber', widget=ForeignKeyWidget(Subscriber, 'mame'))
    group = fields.Field(attribute='group', widget=ForeignKeyWidget(GroupLine, 'name'))

    class Meta:
        model = Line


class Line1Admin(ImportExportActionModelAdmin):
    resource_class = LineResourse
    list_display = ['pk', 'name', 'short_name', 'voltage', 'kvl', 'subscriber']
    list_display_links = ['name']
    search_fields = ['name', 'short_name', ]
    list_filter = ['management', 'voltage']


admin.site.register(Line, Line1Admin)



