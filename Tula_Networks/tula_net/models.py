from django.db import models
from django.urls import reverse

from tula_net.utils import to_digit

'''
context_menu = {'substations': 'Подстанции', 'subscribers': 'Абоненты', 'feeders': 'Присоединения',
            'persons': 'Ответственные лица', 'sections': 'Секции', 'phones': 'Телефоны'}

'''


class Group(models.Model):
    name = models.CharField(max_length=64, verbose_name='Группа', unique=True)
    location = models.TextField(verbose_name='Расположение', blank=True)
    description = models.TextField(verbose_name='Описение', blank=True)
    ours = models.BooleanField(verbose_name='наши', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('group', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ['-ours', 'name']


class Res(models.Model):
    name = models.CharField(max_length=32, verbose_name='РЭС', unique=True)
    short_name = models.CharField(max_length=16, verbose_name='РЭС сокращ + участок', unique=True)
    location = models.TextField(verbose_name='Расположение', blank=True)
    description = models.TextField(verbose_name='Описение', blank=True)

    def get_absolute_url(self):
        return reverse('res', kwargs={'pk': self.pk})

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = "РЭС"
        verbose_name_plural = "РЭСы"
        ordering = ['name']


class Substation(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name='Номер ПС', unique=True)
    name = models.CharField(max_length=32, verbose_name='Название ПС', unique=True)
    voltage_h = models.PositiveSmallIntegerField(verbose_name='напряжение высокое', blank=True, null=True)
    voltage_m = models.PositiveSmallIntegerField(verbose_name='напряжение среднее', blank=True, null=True)
    voltage_l = models.PositiveSmallIntegerField(verbose_name='напряжение низкое', blank=True, null=True)
    alien = models.BooleanField(verbose_name='абонентская?')
    owner = models.ForeignKey('Subscriber', related_name='substations', verbose_name='Владелец',
                              on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(Group, related_name='substations', verbose_name='Группа',
                              on_delete=models.SET_NULL, blank=True, null=True)
    location = models.TextField(verbose_name='Расположение', blank=True)
    description = models.TextField(verbose_name='Описение', blank=True)

    def get_absolute_url(self):
        return reverse('substation', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подстанция"
        verbose_name_plural = "Подстанции"
        ordering = ['number']


class Section(models.Model):
    substation = models.ForeignKey(Substation, related_name='sections', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, verbose_name='Название секции')
    voltage = models.PositiveSmallIntegerField(verbose_name='напряжение')
    description = models.TextField(verbose_name='Описение', blank=True)

    def get_absolute_url(self):
        return reverse('section', kwargs={'pk': self.pk})

    def __str__(self):
        return ' '.join((str(self.name), 'ПС', str(self.substation)))

    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"
        ordering = ['name']


class Subscriber(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название организации', unique=True)
    short_name = models.CharField(max_length=16, verbose_name='Назв орган сокращ', blank=True, null=True)
    ours = models.BooleanField(verbose_name='наши')
    year_update = models.PositiveSmallIntegerField(verbose_name='Списки обновлены', blank=True, null=True)
    description = models.TextField(verbose_name='Описение', blank=True)

    def get_absolute_url(self):
        return reverse('subscriber', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "организация"
        verbose_name_plural = "организации"
        ordering = ['-ours', 'name']


class Person(models.Model):
    name = models.CharField(max_length=64, verbose_name='ФИО')
    subscriber = models.ForeignKey(Subscriber, related_name='persons', on_delete=models.CASCADE)
    position = models.CharField(max_length=64, verbose_name='должность', blank=True, null=True)
    priority = models.PositiveSmallIntegerField(blank=True, verbose_name='приоритет', null=True)
    description = models.TextField(verbose_name='Описение', blank=True)

    def get_absolute_url(self):
        return reverse('person', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ответственное лицо"
        verbose_name_plural = "Ответственные лица"
        ordering = ['priority']


class Feeder(models.Model):
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
    in_reserve = models.BooleanField(default=False, verbose_name='Резервный')
    description = models.TextField(verbose_name='Описение', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('feeder', kwargs={'pk': self.pk})

    def __str__(self):
        return ' '.join(('фид', str(self.name), str(self.substation)))

    class Meta:
        verbose_name = "фидер"
        verbose_name_plural = "фидера"
        ordering = ['section', 'subscriber', 'name']


class Phone(models.Model):
    number = models.CharField(max_length=16, verbose_name='номер')
    search_number = models.CharField(max_length=16, verbose_name='НЕ ЗАПОЛНЯТЬ', blank=True, null=True)
    mail = models.EmailField(max_length=32, verbose_name='электронка', blank=True)
    subscriber = models.ForeignKey(Subscriber, related_name='phones', on_delete=models.CASCADE,
                                   blank=True, null=True, verbose_name='организация')
    person = models.ForeignKey(Person, related_name='phones', on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name='лицо')
    substation = models.ForeignKey(Substation, related_name='phones', on_delete=models.CASCADE,
                                   blank=True, null=True, verbose_name='ПС')
    priority = models.PositiveSmallIntegerField(blank=True, verbose_name='приоритет', null=True)
    description = models.TextField(verbose_name='описение', blank=True)

    # only_digit = to_digit(number)

    def get_absolute_url(self):
        return reverse('phone', kwargs={'pk': self.pk})

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"
        ordering = ['priority']
