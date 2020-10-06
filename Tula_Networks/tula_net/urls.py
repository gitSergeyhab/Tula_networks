from django.contrib import admin
from django.urls import path

from tula_net.views import Main, PsList, GroupPS, ResPS, OnePS, SectionList, OneSection, OneSubstation, SectionPS, \
    SubscriberList, OneSubscriber, SubscribersBySection, SubscribersByPS, SubstationsBySubscriber, SearcherSubscribers, \
    SearcherPS, SearcherPersons, AllFeeders, OneFeeders, OnePerson, PersonList, AddFeeder, UpdFeeder, \
    SubscriberAutocomplete, SubstationAutocomplete

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('substations/', PsList.as_view(), name='substations'),
    path('group/<int:pk>/', GroupPS.as_view(), name='group'),
    # path('res/<int:pk>/', ResPS.as_view(), name='res'),
    path('substations/<int:pk>/', OnePS.as_view(), name='substation'),
    path('sections/', SectionList.as_view(), name='sections'),
    path('section_ps/<int:pk>/', SectionPS.as_view(), name='section_ps'),

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

    # 1 лист всех людей, 2 карточка 1-го человека
    path('persons/', PersonList.as_view(), name='persons'),
    path('person/<int:pk>/', OnePerson.as_view(), name='person'),

    # один абонент со списком ПС со списком фидеров
    path('substations/subscriber/<int:pk>/', SubstationsBySubscriber.as_view(), name='subscriber_ss'),

    # поиски 1. по абонента(полное и сокращеное имя), 2. по ПС, 3. по людям
    path('searcher_subscribers/', SearcherSubscribers.as_view(), name='searcher_subscribers'),
    path('searcher_substations/', SearcherPS.as_view(), name='searcher_substations'),
    path('searcher_persons/', SearcherPersons.as_view(), name='searcher_persons'),

    # формы 1-2.ПС, 3-4.Фид, 5-6.Абонент
    # path('add_PS/', AddPS.as_view(), name='add_PS'),
    # path('upd_PS/', UpdPS.as_view(), name='upd_PS'),
    path('add_feeder/<int:pk>/', AddFeeder.as_view(), name='add_feeder'),

    path('upd_feeder/<int:pk>/', UpdFeeder.as_view(), name='upd_feeder'),

    path('subscriber_autocomplete/', SubscriberAutocomplete.as_view(), name='subscriber_autocomplete'),
    path('substation_autocomplete/', SubstationAutocomplete.as_view(), name='substation_autocomplete'),





]
