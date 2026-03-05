from django.urls import path

from tresorerie.controllers.TreasuryController import facture_client_page, facture_fournisseur_page, new_paiement_client, new_paiement_fournisseur, newFactureClient, newFactureFournisseur, tresorerie_page

urlpatterns = [
    path('treasury_page/', tresorerie_page, name='tresorerie_page'),
    path('invoice_client_page/', facture_client_page, name='facture_client_page'),
    path('invoice_supplier_page/', facture_fournisseur_page, name='facture_fournisseur_page'),
    path('new_invoice_client/', newFactureClient, name='new_facture_client'),
    path('new_invoice_supplier/', newFactureFournisseur, name='new_facture_fournisseur'),
    path('new_payment_client/', new_paiement_client, name='new_paiement_client'),
    path('new_payment_supplier/', new_paiement_fournisseur, name='new_paiement_fournisseur'),
]