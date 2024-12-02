from django.urls import path

from .views import *
from functools import partial

app_name = 'klaen'
urlpatterns = [
     path('api/indoor-buildthing-updated/', indoorBuildthingUpdated, name='indoor-buildthing-updated'),
     path('api/data-capacity/', dataCapacity, name='data-capacity'),
    path('api/eda-index/', eda_index, name='eda-index'),
    path('api/eda-process/', exploratory_data_analysis, name='eda-process'),
    path('api/indoor-arduino/', indoor_arduino_index, name='indoor-arduino'),
    path('api/buildthing-index/', indoor_buildthing_index, name='buildthing-index'),
    path('api/outdoor-weather/', outdoor_weather_index, name='outdoor-weather'),
    path('api/indoor-plalion-data/', indoorPlalionData, name='indoor-plalion-data'),
    path('api/download-data-type/', downloadDataByType, name='download-data-type'),
    path('api/klaen-index/', indoor_klaen_index, name='klaen-index'),
    path('api/indoor-plalion-company-data/', indoorPlalionDataCompany, name='indoor-plalion-company-data'),
    path('api/klaen-company-index/', indoor_klaen_company_index, name='klaen-company-index'),
    path('api/get-sensor-data-updated/',  get_sensor_data_updated, name='get-sensor-data-updated'),
    path('api/display-weather-updated/', displayDataFromAPIUpdated, name='display-weather-updated'),

    # new path code
    path('api/plalion-sensor/', get_unique_serial_numbers, name='plalion-sensor'),
    path('api/plalion-sensor-mqtt/', get_latest_sensor_mqtt, name='plalion-sensor-mqtt'),
    path('device-management/', device_management, name='device-management'),
    path('device-management-2/', device_management_2, name='device-management-2'),
    
    # New update November
    path('klaen-data', klaen_data, name='klaen-data'),
    path('api/get-all-kits', get_all_kits_data, name='get-all-kits'),
    path('chart-sn', chart_sn, name='chart-sn'),
    path('api/get-chart-sn', get_chart_sn, name='get-chart-sn'),
    
    
   
    
]
