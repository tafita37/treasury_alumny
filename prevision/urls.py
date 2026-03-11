from django.urls import path

from prevision.controllers.ForeCastController import prevision_budgetaire_page, prevision_chart_data, prevision_chart_data_decaissement, prevision_chart_data_encaissement, prevision_decaissement_page, prevision_encaissement_page, prevision
urlpatterns = [
    path('cash_inflow_forecast_page/', prevision_encaissement_page, name='prevision_encaissement_page'),
    path('cash_outflow_forecast_page/', prevision_decaissement_page, name='prevision_decaissement_page'),
    path('forecast_validate/', prevision, name='prevision'),
    path('forecast_financial_page/', prevision_budgetaire_page, name='prevision_budgetaire_page'),
    path('forecast_financial_data/', prevision_chart_data, name='prevision_chart_data'),
    path('forecast_financial_data_inflow/', prevision_chart_data_encaissement, name='prevision_chart_data_encaissement'),
    path('forecast_financial_data_outflow/', prevision_chart_data_decaissement, name='prevision_chart_data_decaissement'),
]