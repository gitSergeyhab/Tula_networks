
from django.contrib import admin
from django.urls import path

from tula_net.views import Main, PsList, GroupPS, ResPS, OnePS, SectionList, OneSection, OneSubstation, SectionPS, \
   SubscriberList, OneSubscriber, SubscribersBySection, SubscribersByPS, SubstationsBySubscriber, SearcherSubscribers, \
   SearcherPS, AllFeeders, OneFeeders

urlpatterns = [
   path('', Main.as_view(), name='main'),
   path('substations/', PsList.as_view(), name='substations'),
   path('group/<int:pk>/', GroupPS.as_view(), name='group'),
   # path('res/<int:pk>/', ResPS.as_view(), name='res'),
   path('substations/<int:pk>/', OnePS.as_view(), name='substation'),
   path('sections/', SectionList.as_view(), name='sections'),
   path('section_ps/<int:pk>/', SectionPS.as_view(), name='section_ps'),

   path('feeders/', AllFeeders.as_view(), name='feeders'),
   path('feeder/<int:pk>/', OneFeeders.as_view(), name='feeder'),
   path('feeders/section/<int:pk>/', OneSection.as_view(), name='section'),
   path('feeders/substation/<int:pk>/', OneSubstation.as_view(), name='substation_f'),

   path('subscribers/', SubscriberList.as_view(), name='subscribers'),
   path('subscriber/<int:pk>/', OneSubscriber.as_view(), name='subscriber'),

   # одна СкШ или ПС со списком абонентов со списком фидеров
   path('subscribers/section/<int:pk>/', SubscribersBySection.as_view(), name='subscriber_sec'),
   path('subscribers/substation/<int:pk>/', SubscribersByPS.as_view(), name='subscriber_ps'),

   # один абонент со списком ПС со списком фидеров
   path('substations/subscriber/<int:pk>/', SubstationsBySubscriber.as_view(), name='subscriber_ss'),

   path('searcher_subscribers/', SearcherSubscribers.as_view(), name='searcher_subscribers'),
   path('searcher_substations/', SearcherPS.as_view(), name='searcher_substations'),

]
