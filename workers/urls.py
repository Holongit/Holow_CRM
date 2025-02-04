from django.urls import path

from workers.views import *


urlpatterns = [
    path('', workers, name='workers'),
    path('filters_work/<str:status>/', filters_work_change, name='filters_work_change'),
    path('workers_list/<int:pk>/', workers_gad_list, name='workers_list'),
    path('gadget_info/<int:pk>', GadgetInfo.as_view(), name='gadget_info'),
    path('add_gadget_to_worker/<int:pk>', add_gadget_to_worker, name='add_gadget_to_worker'),
    path('delete_gadget_to_worker/<int:pk>', delete_gadget_to_worker, name='delete_gadget_to_worker'),
    path('odstawic_gadget/<int:pk>', odstawic_gadget, name='odstawic_gadget'),
    path('odstawoc_rezygnacja_gadget/<int:pk>', odstawic_rezygnacja_gadget, name='oodstawoc_rezygnacja_gadget'),
    path('location_cng/<int:pk><str:location_id>', gadget_location_change, name='gadget_location_change'),
]
