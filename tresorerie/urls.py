from django.urls import path

from tresorerie.controllers.TreasuryController import facture_client_page, facture_fournisseur_page, facture_regler_page, get_solde_actuel, mouvement_argent_page, new_mouvement_argent, new_paiement_client, new_paiement_fournisseur, new_paiements, newFactureClient, newFactureFournisseur, tresorerie_page

urlpatterns = [
    path('treasury_page/', tresorerie_page, name='tresorerie_page'),
    path('invoice_client_page/', facture_client_page, name='facture_client_page'),
    path('invoice_supplier_page/', facture_fournisseur_page, name='facture_fournisseur_page'),
    path('new_invoice_client/', newFactureClient, name='new_facture_client'),
    path('new_invoice_supplier/', newFactureFournisseur, name='new_facture_fournisseur'),
    path('new_payment_client/', new_paiement_client, name='new_paiement_client'),
    path('new_payment_supplier/', new_paiement_fournisseur, name='new_paiement_fournisseur'),
    path('financial_transaction_page/', mouvement_argent_page, name='mouvement_argent_page'),
    path('new_financial_transaction/', new_mouvement_argent, name='new_mouvement_argent'),
    path('paid_invoice_page/', facture_regler_page, name='facture_regler_page'),
    path('actual_solde/', get_solde_actuel, name='get_solde_actuel'),
    path('new_payments/', new_paiements, name='new_paiements'),
]