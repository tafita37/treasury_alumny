# views.py
import json
from django.utils import timezone

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from Constantes import MONTH_NAMES
from prevision.metier.Forecast import Forecast

@require_GET
@login_required(login_url='login_user_page') 
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
                'cash_outflow': f.cash_outflow,
                'prevision_id' : f.id
            })
        else:
            forecasts.append({
                'months': month,
                'month_name': MONTH_NAMES[month],
                'years': year,
                'cash_inflow': 0,
                'cash_outflow': 0,
                'prevision_id' : ''
            })
    return render(request, "views/prevision_encaissement.html", {'forecasts': forecasts, 'year': year})

@require_GET
@login_required(login_url='login_user_page') 
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
                'cash_outflow': f.cash_outflow,
                'prevision_id' : f.id
            })
        else:
            forecasts.append({
                'months': month,
                'month_name': MONTH_NAMES[month],
                'years': year,
                'cash_inflow': 0,
                'cash_outflow': 0,
                'prevision_id' : ''
            })
    return render(request, "views/prevision_decaissement.html", {'forecasts': forecasts, 'year': year})

@require_POST
@login_required(login_url='login_user_page') 
def prevision(request):
    data = json.loads(request.body)
    prevision_id=data.get('prevision_id')
    month = data.get('month')
    cash_inflow = data.get('cash_inflow')
    cash_outflow = data.get('cash_outflow')
    year = data.get('year')
    if prevision_id:
        forecast=Forecast.objects.filter(id=prevision_id).first()
        if cash_inflow is None:
            cash_inflow = forecast.cash_inflow
        if cash_outflow is None:
            cash_outflow = forecast.cash_outflow
        Forecast.objects.filter(id=prevision_id).update(
            cash_inflow=cash_inflow,
            cash_outflow=cash_outflow
        )
    else :
        if cash_inflow is None:
            cash_inflow = 0
        if cash_outflow is None:
            cash_outflow = 0
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
@login_required(login_url='login_user_page') 
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
                'cash_outflow': f.cash_outflow,
                'prevision_id' : f.id
            })
        else:
            forecasts.append({
                'months': month,
                'month_name': MONTH_NAMES[month],
                'years': year,
                'cash_inflow': 0,
                'cash_outflow': 0,
                'prevision_id' : ''
            })
    return render(request, "views/prevision_budgetaire.html", {'forecasts': forecasts, 'year': year})

@require_GET
@login_required(login_url='login_user_page') 
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