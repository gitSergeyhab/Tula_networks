import pandas as pd

from .models import Subscriber, Substation, Group, Section, Feeder, Feeder_characteristic

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


f5 = pd.read_excel('tula_net/data_lists/f7.xlsx')


def feeder_plus(feeders):
    repeat = []
    for i, f in feeders.iterrows():
        if i not in repeat:
            # print(f['name_f'],f['name_ps'], f['long'] )
            try:
                charac = Feeder_characteristic.objects.create(
                    feeder_name=f['name_f'],
                    substation_name=f['name_ps'],
                    # feeder=Feeder.objects.filter(name=f['name_f'], substation__name=f['name_ps'])[0],
                    length=f['long'],
                    tp_our_num=f['tp_te'],
                    tp_alien_num=f['tp_al'],
                    villages_num=f['vil_num'],
                    villages_names=f['vil_name'],
                    power_winter=f['pow_win'],
                    power_summer=f['pow_sum'],
                    population=f['peop_num'],
                    points=f['points'],
                    social_num=f['szo_num'],
                    social_names=f['szo_name'],
                )
            except:
                print(f['name_f'], f['name_ps'], '!!!')
            print(i, f['name_f'], f['name_ps'], "+")
            repeat.append(i)


def numeric_feeder_maker():
    for f in Feeder.objects.all():
        print(f.try_number_name)

