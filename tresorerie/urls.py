from django.urls import path

from tresorerie.controllers.TresorerieController import tresorerie_page

urlpatterns = [
    path('treasury_page/', tresorerie_page, name='tresorerie_page'),
]