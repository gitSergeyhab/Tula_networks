from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from tula_net.views import MainView, PsListView, GroupPSView, VoltPSView, OnePSView, SectionListView, OneSectionView, \
    OneSubstationView, SubscriberListView, OneSubscriberView, SubscribersBySectionView, \
    SubscribersByPSView, SubstationsBySubscriberView, SearcherSubscribersView, SearcherPSView, SearcherPersonsView, \
    AllFeedersView, OneFeedersView, OnePersonView, PersonListView, OnePhoneView, PhoneListView, AddFeederFromPSView, \
    UpdFeederView, UpdPhoneView, SubscriberAutocompleteView, SubstationAutocompleteView, AddPersonPhoneView, \
    SearcherPhonesView, AddPSPhoneView, AddSubscriberPhoneView, PhoneDeleteView, FeederDeleteView, AddSubscriberView, \
    UpdSubscriberView, SubscriberDeleteView, AddPersonView, UpdPersonView, DelPersonView, UpdSubstationView, \
    AddFeederFromSubscriberView, AddSectionFromPSView, UpdSectionView,  AddFeederFromSecView, \
    AddSubstationView, LinesGroupView, LinesVoltageView, LinesRegionView, \
    UpdLineView, LineDeleteView, SectionDeleteView, SearcherLinesView, Lines1View, OneLine1View, AddLine1View, \
    Section1View, SearcherFeedersView, FeedersView, MyLogin

urlpatterns = [
    path('in', MyLogin.as_view(), name='in'),
    path('out', LogoutView.as_view(), name='out'),
    path('', MainView.as_view(), name='main'),

    # ПС
    path('substations/', PsListView.as_view(), name='substations'),
    path('substation/<int:pk>/', OnePSView.as_view(), name='substation'),
    path('group/<int:pk>/', GroupPSView.as_view(), name='group'),
    path('voltage/<int:pk>/', VoltPSView.as_view(), name='voltage'),
    # одна ПС со списком секций - секция со списком фидеров:
    # path('section_ps/<int:pk>/', SectionPSView.as_view(), name='section_ps'),

    # СкШ
    path('section/<int:pk>/', Section1View.as_view(), name='one_section'),
    path('sections/', SectionListView.as_view(), name='sections'),

    # 1 лист всех фидеров, 2 карточка 1-го фидера, 3-4 все фидера по секции-подстаннции

    path('sfeeders/', FeedersView.as_view(), name='sfeeders'),
    path('feeders/', AllFeedersView.as_view(), name='feeders'),
    path('feeder/<int:pk>/', OneFeedersView.as_view(), name='feeder'),
    path('feeders/section/<int:pk>/', OneSectionView.as_view(), name='section'),
    path('feeders/substation/<int:pk>/', OneSubstationView.as_view(), name='substation_f'),

    # 1 лист всех абонентов, 2 карточка 1-го абонента, 3-4 одна СкШ или ПС со списком абонентов со списком фидеров
    path('subscribers/', SubscriberListView.as_view(), name='subscribers'),
    path('subscriber/<int:pk>/', OneSubscriberView.as_view(), name='subscriber'),
    path('subscribers/section/<int:pk>/', SubscribersBySectionView.as_view(), name='subscriber_sec'),
    path('subscribers/substation/<int:pk>/', SubscribersByPSView.as_view(), name='subscriber_ps'),
    # один абонент со списком ПС со списком фидеров
    path('substations/subscriber/<int:pk>/', SubstationsBySubscriberView.as_view(), name='subscriber_ss'),

    # 1 лист всех людей, 2 карточка 1-го человека
    path('persons/', PersonListView.as_view(), name='persons'),
    path('person/<int:pk>/', OnePersonView.as_view(), name='person'),

    # 1 лист всех телефонов, 2 карточка 1-го телефона
    path('phones/', PhoneListView.as_view(), name='phones'),
    path('phone/<int:pk>/', OnePhoneView.as_view(), name='phone'),

    # 1 лист всех ВЛ, 2 карточка 1-й ВЛ
    path('lines/', Lines1View.as_view(), name='lines'),
    path('line/<int:pk>/', OneLine1View.as_view(), name='line'),
    path('line_group/<int:pk>/', LinesGroupView.as_view(), name='line_group'),
    path('line_voltage/<int:pk>/', LinesVoltageView.as_view(), name='line_voltage'),
    path('line_region/<int:pk>/', LinesRegionView.as_view(), name='line_region'),

    # поиски 1. по абонента(полное и сокращеное имя), 2. по ПС, 3. по людям, 4. телефонам
    path('searcher_subscribers/', SearcherSubscribersView.as_view(), name='searcher_subscribers'),
    path('searcher_substations/', SearcherPSView.as_view(), name='searcher_substations'),
    path('searcher_persons/', SearcherPersonsView.as_view(), name='searcher_persons'),
    path('searcher_phones/', SearcherPhonesView.as_view(), name='searcher_phones'),
    path('searcher_lines/', SearcherLinesView.as_view(), name='searcher_lines'),
    path('searcher_feeders/', SearcherFeedersView.as_view(), name='searcher_feeders'),
    # формы
    # фидера 1.добавление с ПС, 2. !... от абонента! 3.обновление, 4. удаление
    path('add_feeder/from_ps_pk/<int:pk>/', AddFeederFromPSView.as_view(), name='add_feeder_from_ps'),
    path('add_feeder/from_ss_pk/<int:pk>/', AddFeederFromSubscriberView.as_view(), name='add_feeder_from_ss'),
    path('add_feeder/from_sec_pk/<int:pk>/', AddFeederFromSecView.as_view(), name='add_feeder_from_sec'),
    path('upd_feeder/<int:pk>/', UpdFeederView.as_view(), name='upd_feeder'),
    path('del_feeder/<int:pk>/', FeederDeleteView.as_view(), name='del_feeder'),
    # абоненты
    path('add_subscriber/', AddSubscriberView.as_view(), name='add_subscriber'),
    path('upd_subscriber/<int:pk>/', UpdSubscriberView.as_view(), name='upd_subscriber'),
    path('del_subscriber/<int:pk>', SubscriberDeleteView.as_view(), name='del_subscriber'),
    # лица
    path('add_person/from_ss_pk/<int:pk>/', AddPersonView.as_view(), name='add_person'),
    path('upd_person/<int:pk>/', UpdPersonView.as_view(), name='upd_person'),
    path('del_person/<int:pk>/', DelPersonView.as_view(), name='del_person'),
    # телефоны добавление 1. от лица, 2. от абонента, 3. от ПС, 4, 5
    path('add_phone/from_person_pk/<int:pk>/', AddPersonPhoneView.as_view(), name='add_phone_p'),
    path('add_phone/from_subscriber_pk/<int:pk>/', AddSubscriberPhoneView.as_view(), name='add_phone'),
    path('add_phone/from_substation_pk/<int:pk>/', AddPSPhoneView.as_view(), name='add_phone_ps'),
    path('upd_phone/<int:pk>/', UpdPhoneView.as_view(), name='upd_phone'),
    path('del_phone/<int:pk>/', PhoneDeleteView.as_view(), name='del_phone'),
    # ПС
    path('add_substation/', AddSubstationView.as_view(), name='add_substation'),
    path('upd_substation/<int:pk>', UpdSubstationView.as_view(), name='upd_substation'),
    # СкШ
    path('add_section/from_ps_pk/<int:pk>/', AddSectionFromPSView.as_view(), name='add_section'),
    path('upd_section/<int:pk>/', UpdSectionView.as_view(), name='upd_section'),
    path('del_section/<int:pk>/', SectionDeleteView.as_view(), name='del_section'),

    path('add_line/', AddLine1View.as_view(), name='add_line'),
    path('upd_line/<int:pk>/', UpdLineView.as_view(), name='upd_line'),
    path('del_line/<int:pk>/', LineDeleteView.as_view(), name='del_line'),

    # !не работают!
    path('subscriber_autocomplete/', SubscriberAutocompleteView.as_view(), name='subscriber_autocomplete'),
    path('substation_autocomplete/', SubstationAutocompleteView.as_view(), name='substation_autocomplete'),

]
