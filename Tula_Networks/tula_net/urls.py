from django.contrib import admin
from django.urls import path

from tula_net.views import Main, PsList, GroupPS, VoltPS, OnePS, SectionList, OneSection, OneSubstation, SectionPS, \
    SubscriberList, OneSubscriber, SubscribersBySection, SubscribersByPS, SubstationsBySubscriber, \
    SearcherSubscribers, SearcherPS, SearcherPersons, AllFeeders, OneFeeders, OnePerson, PersonList, OnePhone, \
    PhoneList, AddFeeder, UpdFeeder, UpdPhone, SubscriberAutocomplete, SubstationAutocomplete, AddPersonPhone, \
    SearcherPhones, AddPSPhone, AddSubscriberPhone, PhoneDelete, FeederDelete, AddSubscriber, UpdSubscriber, \
    SubscriberDelete, AddPerson, UpdPerson, DelPerson, UpdSubstation

urlpatterns = [
    path('', Main.as_view(), name='main'),

    # ПС
    path('substations/', PsList.as_view(), name='substations'),
    path('substation/<int:pk>/', OnePS.as_view(), name='substation'),
    path('group/<int:pk>/', GroupPS.as_view(), name='group'),
    path('voltage/<int:pk>/', VoltPS.as_view(), name='voltage'),
    # одна ПС со списком секций - секция со списком фидеров:
    path('section_ps/<int:pk>/', SectionPS.as_view(), name='section_ps'),

    # СкШ
    path('sections/', SectionList.as_view(), name='sections'),

    # 1 лист всех фидеров, 2 карточка 1-го фидера, 3-4 все фидера по секции-подстаннции
    path('feeders/', AllFeeders.as_view(), name='feeders'),
    path('feeder/<int:pk>/', OneFeeders.as_view(), name='feeder'),
    path('feeders/section/<int:pk>/', OneSection.as_view(), name='section'),
    path('feeders/substation/<int:pk>/', OneSubstation.as_view(), name='substation_f'),

    # 1 лист всех абонентов, 2 карточка 1-го абонента, одна СкШ или ПС со списком абонентов со списком фидеров
    path('subscribers/', SubscriberList.as_view(), name='subscribers'),
    path('subscriber/<int:pk>/', OneSubscriber.as_view(), name='subscriber'),
    path('subscribers/section/<int:pk>/', SubscribersBySection.as_view(), name='subscriber_sec'),
    path('subscribers/substation/<int:pk>/', SubscribersByPS.as_view(), name='subscriber_ps'),
    # один абонент со списком ПС со списком фидеров
    path('substations/subscriber/<int:pk>/', SubstationsBySubscriber.as_view(), name='subscriber_ss'),

    # 1 лист всех людей, 2 карточка 1-го человека
    path('persons/', PersonList.as_view(), name='persons'),
    path('person/<int:pk>/', OnePerson.as_view(), name='person'),

    # 1 лист всех телефонов, 2 карточка 1-го телефона
    path('phones/', PhoneList.as_view(), name='phones'),
    path('phone/<int:pk>/', OnePhone.as_view(), name='phone'),

    # поиски 1. по абонента(полное и сокращеное имя), 2. по ПС, 3. по людям, 4. телефонам
    path('searcher_subscribers/', SearcherSubscribers.as_view(), name='searcher_subscribers'),
    path('searcher_substations/', SearcherPS.as_view(), name='searcher_substations'),
    path('searcher_persons/', SearcherPersons.as_view(), name='searcher_persons'),
    path('searcher_phones/', SearcherPhones.as_view(), name='searcher_phones'),

    # формы
    # фидера 1.добавление с ПС, 2. !... от абонента! 3.обновление, 4. удаление
    path('add_feeder/from_ps_pk/<int:pk>/', AddFeeder.as_view(), name='add_feeder'),
    path('upd_feeder/<int:pk>/', UpdFeeder.as_view(), name='upd_feeder'),
    path('del_feeder/<int:pk>/', FeederDelete.as_view(), name='del_feeder'),
    # абоненты
    path('add_subscriber/', AddSubscriber.as_view(), name='add_subscriber'),
    path('upd_subscriber/<int:pk>/', UpdSubscriber.as_view(), name='upd_subscriber'),
    path('del_subscriber/<int:pk>', SubscriberDelete.as_view(), name='del_subscriber'),
    # лица
    path('add_person/from_ss_pk/<int:pk>/', AddPerson.as_view(), name='add_person'),
    path('upd_person/<int:pk>/', UpdPerson.as_view(), name='upd_person'),
    path('del_person/<int:pk>/', DelPerson.as_view(), name='del_person'),
    # телефоны добавление 1. от лица, 2. от абонента, 3. от ПС, 4, 5
    path('add_phone/from_person_pk/<int:pk>/', AddPersonPhone.as_view(), name='add_phone_p'),
    path('add_phone/from_subscriber_pk/<int:pk>/', AddSubscriberPhone.as_view(), name='add_phone'),
    path('add_phone/from_substation_pk/<int:pk>/', AddPSPhone.as_view(), name='add_phone_ps'),
    path('upd_phone/<int:pk>/', UpdPhone.as_view(), name='upd_phone'),
    path('del_phone/<int:pk>/', PhoneDelete.as_view(), name='del_phone'),
    # ПС - только изменение
    path('upd_substation/<int:pk>', UpdSubstation.as_view(), name='upd_substation'),

    # !не работают!
    path('subscriber_autocomplete/', SubscriberAutocomplete.as_view(), name='subscriber_autocomplete'),
    path('substation_autocomplete/', SubstationAutocomplete.as_view(), name='substation_autocomplete'),

]
