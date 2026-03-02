# views.py
import json
from django.utils import timezone

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from prevision.metier.Forecast import Forecast

MONTH_NAMES = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre"
}

@require_GET
def prevision_encaissement_page(request):
    year = request.GET.get('year', timezone.now().year)
    print(f"Year: {year}")
    existing_forecasts = {f.months: f for f in Forecast.objects.filter(years=year)}
    
    forecasts = []
    for month in range(1, 13):
        if month in existing_forecasts:
            f = existing_forecasts[month]
            forecasts.append({
                'months': f.months,
                'month_name': MONTH_NAMES[f.months],
                'years': f.years,
                'cash_inflow': f.cash_inflow,
                'cash_outflow': f.cash_outflow
            })
        else:
            forecasts.append({
                'months': month,
                'month_name': MONTH_NAMES[month],
                'years': year,
                'cash_inflow': 0,
                'cash_outflow': 0
            })
    return render(request, "views/prevision_encaissement.html", {'forecasts': forecasts, 'year': year})

@require_GET
def prevision_decaissement_page(request):
    year = request.GET.get('year', timezone.now().year)
    existing_forecasts = {f.months: f for f in Forecast.objects.filter(years=year)}
    
    forecasts = []
    for month in range(1, 13):
        if month in existing_forecasts:
            f = existing_forecasts[month]
            forecasts.append({
                'months': f.months,
                'month_name': MONTH_NAMES[f.months],
                'years': f.years,
                'cash_inflow': f.cash_inflow,
                'cash_outflow': f.cash_outflow
            })
        else:
            forecasts.append({
                'months': month,
                'month_name': MONTH_NAMES[month],
                'years': year,
                'cash_inflow': 0,
                'cash_outflow': 0
            })
    return render(request, "views/prevision_decaissement.html", {'forecasts': forecasts, 'year': year})

@require_POST
def prevision(request):
    data = json.loads(request.body)
    month = data.get('month')
    cash_inflow = data.get('cash_inflow')
    cash_outflow = data.get('cash_outflow')
    year = data.get('year')
    print("year")

    Forecast.objects.update_or_create(
        months=month,
        years=year,
        defaults={
            'cash_inflow': cash_inflow,
            'cash_outflow': cash_outflow
        }
    )

    return JsonResponse({'success': True})

@require_GET
def prevision_budgetaire_page(request):
    year = request.GET.get('year', timezone.now().year)
    existing_forecasts = {f.months: f for f in Forecast.objects.filter(years=year)}
    
    forecasts = []
    for month in range(1, 13):
        if month in existing_forecasts:
            f = existing_forecasts[month]
            forecasts.append({
                'months': f.months,
                'month_name': MONTH_NAMES[f.months],
                'years': f.years,
                'cash_inflow': f.cash_inflow,
                'cash_outflow': f.cash_outflow
            })
        else:
            forecasts.append({
                'months': month,
                'month_name': MONTH_NAMES[month],
                'years': year,
                'cash_inflow': 0,
                'cash_outflow': 0
            })
    return render(request, "views/prevision_budgetaire.html", {'forecasts': forecasts, 'year': year})

@require_GET
def prevision_chart_data(request):
    year = request.GET.get('year', timezone.now().year)
    existing_forecasts = {f.months: f for f in Forecast.objects.filter(years=year)}
    encaissement_prevision = []
    decaissement_prevision = []
    for month in range(1, 13):
        if month in existing_forecasts:
            f = existing_forecasts[month]
            encaissement_prevision.append(f.cash_inflow)
            decaissement_prevision.append(f.cash_outflow)
        else:
            encaissement_prevision.append(0)
            decaissement_prevision.append(0)
    data = {
        "encaissement_prevision": encaissement_prevision,
        "decaissement_prevision": decaissement_prevision,
    }
    return JsonResponse(data)