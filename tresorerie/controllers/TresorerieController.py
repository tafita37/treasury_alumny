# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

@require_GET
@login_required(login_url='login_user_page') 
def tresorerie_page(request):
    return render(request, "views/tresorerie.html")