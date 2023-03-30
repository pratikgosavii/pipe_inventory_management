from django.urls import path

from .views import *
from store import views

urlpatterns = [




    path('fix-stock/', demo, name='demo'),

    
    path('add-inward/', add_inward, name='add_inward'),
    path('update-inward/<inward_id>', update_inward, name='update_inward'),
    path('list-inward/', list_inward, name='list_inward'),

    path('add-outward/', add_outward, name='add_outward'),
    path('update-outward/<outward_id>', update_outward, name='update_outward'),
    path('list-outward/', list_outward, name='list_outward'),

    path('list-stock/', generate_report_stock, name='list_stock'),

    path('report-daily/', generate_report_daily, name='report_daily'),
    path('report-inward/', report_inward, name='report_inward'),
    path('report-outward/', report_outward, name='report_outward'),
    path('report-supply-return/', report_supply_return, name='report_supply_return'),
    path('report-stock/', generate_report_stock, name='generate_report'),

    path('report-main/', generate_report_main, name='generate_report_main'),

    path('download', download, name='download'),

    #delete urls 

    path('delete-dashboard', delete_dashboard, name='delete_dashboard'),
    
    path('list-inward-delete/', list_inward_delete, name='list_inward_delete'),
    path('list-outward-delete/', list_outward_delete, name='list_outward_delete'),
    path('list-return-delete/', list_return_delete, name='list_return_delete'),

    path('delete-inward/<inward_id>', delete_inward, name='delete_inward'),
    path('delete-outward/<outward_id>', delete_outward, name='delete_outward'),
    path('delete-return/<return_id>', delete_return, name='delete_return'),


    path("download-gate-pass/<outward_id>", ResultList, name="list"),






]