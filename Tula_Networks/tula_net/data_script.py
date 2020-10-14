import pandas as pd

from .models import Subscriber, Substation, Group, Section, Feeder

pstula = pd.read_csv('tula_net/data_lists/for_subscribers.csv')
only_subsribers = pstula.subscriber.unique()


def adder_subsriber(only_subsribers):
    repeat = []
    if Subscriber.objects.count() < len(only_subsribers):
        for i in only_subsribers:
            if i not in repeat:
                sub = Subscriber.objects.create(name=i, ours=False)
                repeat.append(i)
    if not Subscriber.objects.filter(name='Тулэнерго'):
        sub = Subscriber.objects.create(name='Тулэнерго', ours=True)


only_pst = pd.read_csv('tula_net/data_lists/only_pst.csv')


def adder_ps(only_pst):
    repeat = []
    if Substation.objects.count() < int(only_pst.number.count()):
        for i, ps in only_pst.iterrows():
            if ps['number'] not in repeat:
                subst = Substation.objects.create(
                    number=ps['number'],
                    name=ps['name'],
                    voltage_l=ps['voltage_l'],
                    alien=False,
                    owner=Subscriber.objects.get(name='Тулэнерго'),
                    group=Group.objects.get(name='Северная'),
                    region='Тула',
                )
                repeat.append(ps['number'])


only_sec = pd.read_csv('tula_net/data_lists/only_sec.csv')


def adder_sec(only_sec):
    repeat = []
    if Section.objects.count() < int(only_pst.number.count()):
        for i, sec in only_sec.iterrows():
            if sec['fake_sect'] not in repeat:
                subst = Section.objects.create(
                    substation=Substation.objects.get(name=sec['name']),
                    name=sec['sec_short'],
                    voltage=sec['voltage_l'],
                )
                repeat.append(sec['fake_sect'])


feeds = pd.read_csv('tula_net/data_lists/pst_fid_secnn2.csv')


def adder_feed(feeds):
    repeat = []
    if Feeder.objects.count() < int(feeds.number.count()):

        for i, f in feeds.iterrows():

            if f['Unnamed: 0'] not in repeat:
                print(f.name_feeder_T, f['name'])
                try:
                    feeder = Feeder.objects.create(
                        substation=Substation.objects.filter(name=f['name'])[0],
                        # section=Section.objects.filter(name=f['sec_short'], substation=f['name'])[0],
                        name=f['name_feeder_T'],
                        subscriber=Subscriber.objects.filter(name=f['subscriber'])[0],
                        region='Тула',
                    )
                except:
                    print(f.name_feeder_T, f['name'])
                print(f.name_feeder_T)
                repeat.append(f['Unnamed: 0'])

# name = models.CharField(max_length=32, verbose_name='Название фидера')
# substation = models.ForeignKey(Substation, related_name='feeders', on_delete=models.CASCADE, verbose_name='ПС')
# section = models.ForeignKey(Section, related_name='feeders', on_delete=models.CASCADE, verbose_name='СкШ')
# subscriber = models.ForeignKey(Subscriber, related_name='feeders', on_delete=models.SET_NULL,
#                                verbose_name='абонент', blank=True, null=True)
# length = models.PositiveSmallIntegerField(blank=True, verbose_name='Протяженность', null=True)
# number_tp = models.PositiveSmallIntegerField(blank=True, verbose_name='Количество ТП', null=True)
# population = models.PositiveSmallIntegerField(blank=True, verbose_name='Население', null=True)
# social = models.PositiveSmallIntegerField(blank=True, verbose_name='Социалка', null=True)
# res = models.ForeignKey(Res, related_name='feeders', verbose_name='РЭС или еще кто',
#                         on_delete=models.SET_NULL, blank=True, null=True)
# attention = models.BooleanField(verbose_name='!!!')
# reliability_category = models.PositiveSmallIntegerField(blank=True, verbose_name='категория надежности', null=True)
# in_reserve = models.BooleanField(default=False, verbose_name='Резервный')
# region = models.CharField(blank=True, max_length=32, verbose_name='Участок', null=True)
# description = models.TextField(verbose_name='Описение', blank=True, null=True)
