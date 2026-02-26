# views.py
from django.shortcuts import render
from django.views.decorators.http import require_GET

@require_GET
def tresorerie_page(request):
    return render(request, "views/tresorerie.html")