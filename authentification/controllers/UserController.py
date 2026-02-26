# views.py
from django.shortcuts import render
from django.views.decorators.http import require_GET

@require_GET
def login_user_page(request):
    return render(request, "views/login_user.html")