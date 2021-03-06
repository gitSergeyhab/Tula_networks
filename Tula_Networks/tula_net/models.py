from django.db import models
from django.urls import reverse


class Region(models.Model):
    name = models.CharField(max_length=128, verbose_name='Регион', unique=True)
    for_menu = models.BooleanField(default=False, verbose_name='Добавить в меню')

    def get_line_url(self):
        return reverse('line_region', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регион"

    def __str__(self):
        return self.name


class ClassVoltage(models.Model):
    class_voltage = models.SmallIntegerField(verbose_name='Класс напряжения')

    def get_absolute_url(self):
        return reverse('voltage', kwargs={'pk': self.pk})

    def get_line_url(self):
        return reverse('line_voltage', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "напряжение"
        verbose_name_plural = "напряжения"
        ordering = ['-class_voltage']

    def __str__(self):
        return ' '.join((str(self.class_voltage), 'кВ'))


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


class GroupLine(models.Model):
    name = models.CharField(max_length=64, verbose_name='Группа', unique=True)
    location = models.TextField(verbose_name='Расположение', blank=True)
    description = models.TextField(verbose_name='Описение', blank=True)
    ours = models.BooleanField(verbose_name='наши', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('line_group', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Участок сл ВЛ"
        verbose_name_plural = "Участки сл ВЛ"
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
    voltage_h = models.ForeignKey(
        ClassVoltage, verbose_name='напряжение высокое', related_name='ps_volt_h',
        blank=True, null=True, on_delete=models.PROTECT)
    voltage_m = models.ForeignKey(
        ClassVoltage, verbose_name='напряжение среднее', related_name='ps_volt_m',
        blank=True, null=True, on_delete=models.PROTECT)
    voltage_l = models.ForeignKey(
        ClassVoltage, verbose_name='напряжение низкое', related_name='ps_volt_l',
        blank=True, null=True, on_delete=models.PROTECT)
    alien = models.BooleanField(verbose_name='чужая?')
    owner = models.ForeignKey('Subscriber', related_name='substations', verbose_name='Владелец',
                              on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(Group, related_name='substations', verbose_name='Группа',
                              on_delete=models.CASCADE)
    location = models.TextField(verbose_name='Расположение', blank=True)
    region = models.ForeignKey(Region, verbose_name='Участок', related_name='substations',
                               on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(verbose_name='Описение', blank=True)

    def get_absolute_url(self):
        return reverse('substation', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подстанция"
        verbose_name_plural = "Подстанции"
        # ordering = ['-voltage_h', 'name']
        ordering = ['number']


class Section(models.Model):
    substation = models.ForeignKey(Substation, related_name='sections', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(verbose_name='№ секции', blank=True, null=True)
    name = models.CharField(max_length=32, verbose_name='Название секции')
    voltage = models.ForeignKey(ClassVoltage, verbose_name='напряжение', on_delete=models.PROTECT, blank=True,
                                null=True)
    from_T = models.PositiveSmallIntegerField(verbose_name='питается от/питает Т №', blank=True, null=True)
    blind = models.BooleanField(default=False, verbose_name='Тупиковая')
    description = models.TextField(verbose_name='Описение', blank=True)

    def get_absolute_url(self):
        return reverse('one_section', kwargs={'pk': self.pk})

    def __str__(self):
        return ' '.join((str(self.name), 'ПС', str(self.substation)))

    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"
        ordering = ['voltage__class_voltage', 'name']



class Subscriber(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название организации', unique=True)
    short_name = models.CharField(max_length=16, verbose_name='Назв орган сокращ', blank=True, null=True)
    ours = models.BooleanField(verbose_name='наши')
    year_update = models.PositiveSmallIntegerField(verbose_name='Списки обновлены', blank=True, null=True)
    description = models.TextField(verbose_name='Описение', blank=True)
    region = models.ForeignKey(
        Region, verbose_name='участок', default=2, blank=True, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('subscriber', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "организация"
        verbose_name_plural = "организации"
        ordering = ['-ours', 'name']


class Person(models.Model):
    name = models.CharField(max_length=128, verbose_name='ФИО')
    subscriber = models.ForeignKey(Subscriber, related_name='persons', on_delete=models.CASCADE)
    position = models.CharField(max_length=64, verbose_name='должность', blank=True, null=True)
    priority = models.PositiveSmallIntegerField(blank=True, verbose_name='приоритет', null=True)
    description = models.TextField(verbose_name='Описение', blank=True)

    # mail = models.EmailField(max_length=32, verbose_name='электронка', blank=True)

    def get_absolute_url(self):
        return reverse('person', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ответственное лицо"
        verbose_name_plural = "Ответственные лица"
        ordering = ['-priority']


class Feeder(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название фидера')
    try_number_name = models.SmallIntegerField(blank=True, null=True)
    substation = models.ForeignKey(Substation, related_name='feeders', on_delete=models.CASCADE, verbose_name='ПС')
    section = models.ForeignKey(Section, related_name='feeders', on_delete=models.CASCADE, verbose_name='СкШ',
                                blank=True, null=True)
    subscriber = models.ForeignKey(Subscriber, related_name='feeders', on_delete=models.SET_NULL,
                                   verbose_name='абонент', blank=True, null=True)
    attention = models.BooleanField(verbose_name='!!!', default=False)
    in_reserve = models.BooleanField(default=False, verbose_name='Резервный')
    region = models.ForeignKey(Region, verbose_name='Участок', related_name='feeders',
                               on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(verbose_name='Описение', blank=True, null=True)
    # res = models.CharField(blank=True, max_length=32, verbose_name='РЭС', null=True)
    # reliability_category = models.PositiveSmallIntegerField(blank=True, verbose_name='категория надежности', null=True)

    def get_absolute_url(self):
        return reverse('feeder', kwargs={'pk': self.pk})

    def __str__(self):
        return ' '.join(('фид', str(self.name), 'ПС', str(self.substation)))

    class Meta:
        verbose_name = "фидер"
        verbose_name_plural = "фидера"
        ordering = ['in_reserve', 'section', 'try_number_name', 'name']


class Phone(models.Model):
    number = models.CharField(max_length=20, verbose_name='номер')
    search_number = models.CharField(max_length=16, verbose_name='НЕ ЗАПОЛНЯТЬ', blank=True, null=True)
    subscriber = models.ForeignKey(Subscriber, related_name='phones', on_delete=models.CASCADE,
                                   blank=True, null=True, verbose_name='организация')
    person = models.ForeignKey(Person, related_name='phones', on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name='лицо')
    substation = models.ForeignKey(Substation, related_name='phones', on_delete=models.CASCADE,
                                   blank=True, null=True, verbose_name='ПС')
    priority = models.PositiveSmallIntegerField(blank=True, verbose_name='приоритет', null=True)
    description = models.TextField(verbose_name='описение', blank=True)

    def get_absolute_url(self):
        return reverse('phone', kwargs={'pk': self.pk})

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"
        ordering = ['-priority']


class TransmissionLine(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    full_name = models.CharField(max_length=128, verbose_name='Полное название', blank=True, null=True)
    short_name = models.CharField(max_length=32, verbose_name='Цифровое название', blank=True, default='')
    section = models.ManyToManyField(Section, verbose_name='Секция', related_name='lines0')
    voltage = models.ForeignKey(ClassVoltage, verbose_name='Напряжение', related_name='lines0',
                                on_delete=models.PROTECT)
    management = models.ForeignKey(Region, verbose_name='Управление', related_name='lines_upr0',
                                   on_delete=models.CASCADE, default=2)
    maintenance = models.ManyToManyField(Region, verbose_name='Ведение', related_name='lines_ved0', blank=True)
    subscriber = models.ForeignKey(Subscriber, related_name='lines0', on_delete=models.SET_NULL,
                                   verbose_name='абонент', blank=True, null=True)
    length = models.FloatField(verbose_name='Протяженность', blank=True, null=True)
    number_columns = models.PositiveSmallIntegerField(verbose_name='Количество опор', blank=True, null=True)
    group = models.ForeignKey(GroupLine, related_name='lines0', verbose_name='Участок сл ВЛ',
                              on_delete=models.CASCADE, default=1)
    description = models.TextField(verbose_name='Описение', blank=True, null=True)
    kvl = models.BooleanField(verbose_name='КВЛ?', default=False)

    def get_absolute_url(self):
        return reverse('line0', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Линия - МОДЕЛЬ ЗАМЕНЕНА"
        verbose_name_plural = "Линии - МОДЕЛЬ ЗАМЕНЕНА"
        ordering = ['voltage', 'short_name']


class Line(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    full_name = models.CharField(max_length=128, verbose_name='Полное название', blank=True, null=True)
    short_name = models.CharField(max_length=32, verbose_name='Цифровое название', blank=True, default='')
    ps_p1 = models.PositiveSmallIntegerField('ПС №1')
    sec_p1 = models.PositiveSmallIntegerField('СШ ПС №1')
    ps_p2 = models.PositiveSmallIntegerField('ПС №2', blank=True, null=True)
    sec_p2 = models.PositiveSmallIntegerField('СШ ПС №2', blank=True, null=True)
    ps_m1 = models.PositiveSmallIntegerField('ПС №3', blank=True, null=True)
    sec_m1 = models.PositiveSmallIntegerField('СШ ПС №3', blank=True, null=True)
    ps_m2 = models.PositiveSmallIntegerField('ПС №4', blank=True, null=True)
    sec_m2 = models.PositiveSmallIntegerField('СШ ПС №4', blank=True, null=True)
    ps_m3 = models.PositiveSmallIntegerField('ПС №5', blank=True, null=True)
    sec_m3 = models.PositiveSmallIntegerField('СШ ПС №5', blank=True, null=True)
    ps_m4 = models.PositiveSmallIntegerField('ПС №6', blank=True, null=True)
    sec_m4 = models.PositiveSmallIntegerField('СШ ПС №6', blank=True, null=True)
    voltage = models.ForeignKey(ClassVoltage, verbose_name='Напряжение', related_name='lines', on_delete=models.PROTECT)
    management = models.ForeignKey(Region, verbose_name='Управление', related_name='lines_upr',
                                   on_delete=models.CASCADE, default=2)
    maintenance = models.ManyToManyField(Region, verbose_name='Ведение', related_name='lines_ved', blank=True)
    subscriber = models.ForeignKey(Subscriber, related_name='lines', on_delete=models.SET_NULL,
                                   verbose_name='абонент', blank=True, null=True)
    length = models.FloatField(verbose_name='Протяженность', blank=True, null=True)
    number_columns = models.PositiveSmallIntegerField(verbose_name='Количество опор', blank=True, null=True)
    group = models.ForeignKey(GroupLine, related_name='lines', verbose_name='Участок сл ВЛ',
                              on_delete=models.CASCADE, default=1)
    description = models.TextField(verbose_name='Описение', blank=True, null=True)
    kvl = models.BooleanField(verbose_name='КВЛ?', default=False)

    def get_absolute_url(self):
        return reverse('line', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Линия"
        verbose_name_plural = "Линии"
        ordering = ['voltage', 'short_name']


class Feeder_characteristic(models.Model):
    feeder_name = models.CharField(max_length=64, verbose_name='Название фидера')
    substation_name = models.CharField(max_length=64, verbose_name='Название ПС')
    feeder = models.OneToOneField(Feeder, related_name="character", on_delete=models.SET_NULL,
                                  null=True, blank=True, verbose_name='фидер')
    length = models.FloatField(verbose_name='Протяженность', blank=True, null=True)
    tp_our_num = models.PositiveSmallIntegerField(blank=True, verbose_name='ТП наши: количество', null=True)
    tp_alien_num = models.PositiveSmallIntegerField(blank=True, verbose_name='ТП чужие: количество', null=True)
    villages_num = models.PositiveSmallIntegerField(blank=True, verbose_name='НП количество', null=True)
    villages_names = models.TextField(blank=True, verbose_name='НП названия', null=True)
    power_winter = models.FloatField(verbose_name='Зима МВт', blank=True, null=True)
    power_summer = models.FloatField(verbose_name='Лето МВт', blank=True, null=True)
    population = models.PositiveSmallIntegerField(blank=True, verbose_name='Население', null=True)
    points = models.PositiveSmallIntegerField(blank=True, verbose_name='Точки поставки', null=True)
    social_num = models.PositiveSmallIntegerField(blank=True, verbose_name='Социалка кол-во', null=True)
    social_names = models.TextField(blank=True, verbose_name='Социалка тип', null=True)
    checked = models.BooleanField(verbose_name='соответствует', default=False)

    def get_absolute_url(self):
        return reverse('feeder_char', kwargs={'pk': self.pk})

    def get_upd_url(self):
        return reverse('upd_charact_fl', kwargs={'pk': self.pk})


    def __str__(self):
        return ' '.join(('ПС', self.substation_name, 'фид', self.feeder_name))

    class Meta:
        unique_together = ('feeder_name', 'substation_name')
        verbose_name = "характеристика фидера"
        verbose_name_plural = "х-ки фидеров"

