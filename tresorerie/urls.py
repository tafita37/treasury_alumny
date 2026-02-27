from django.urls import path

from tresorerie.controllers.PrevisionController import prevision_encaissement_page
from tresorerie.controllers.TresorerieController import tresorerie_page

urlpatterns = [
    path('treasury_page/', tresorerie_page, name='tresorerie_page'),
    path('cash_forecast_page/', prevision_encaissement_page, name='prevision_encaissement_page'),
]