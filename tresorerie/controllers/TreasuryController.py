# views.py
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from Constantes import ETAT, MONTHS
from tresorerie.metier.Company import Company
from django.core.paginator import Paginator, EmptyPage
from tresorerie.metier.Invoice import Invoice
from datetime import datetime
from django.db.models import Q
from django.utils import timezone

from tresorerie.metier.Payment import Payment

@require_GET
@login_required(login_url='login_user_page') 
def tresorerie_page(request):
    return render(request, "views/tresorerie.html")

@require_GET
@login_required(login_url='login_user_page')
def facture_client_page(request):
    # Récupération des paramètres
    reference = request.GET.get('reference', '')
    client_id = request.GET.get('client', '')
    annee = request.GET.get('annee', '')
    mois = request.GET.get('mois', '')
    status = request.GET.get('status', '')
    
    # Liste des clients pour le filtre
    listeClient = Company.objects.filter(is_client=True).values('id', 'name')
    
    # Construction des filtres avec Q
    if reference:
        conditions = Q(invoice_number__icontains=reference)
    else:
        conditions = Q()
        
        if client_id:
            conditions &= Q(company_id=client_id)
        if status:
            conditions &= Q(status=status)
        if annee and mois:
            conditions &= Q(invoice_date__year=annee, invoice_date__month=mois)
        elif annee:
            conditions &= Q(invoice_date__year=annee)
        elif mois:
            conditions &= Q(invoice_date__year=timezone.now().year, invoice_date__month=mois)
    
    # Application des filtres
    factures_list = Invoice.objects.filter(is_supplier=False).filter(conditions).order_by('-invoice_date')
    
    # Pagination
    paginator = Paginator(factures_list, 20)
    
    try:
        factures = paginator.page(request.GET.get('page', 1))
    except (EmptyPage, ValueError, TypeError):
        factures = paginator.page(1) if paginator.num_pages > 0 else []
    
    context = {
        'listeClient': listeClient,
        'months': MONTHS,
        'etats': ETAT,
        'factures': factures,
        'paginator': paginator,
        'page_vide': isinstance(factures, list),
        'filtres': {
            'reference': reference,
            'client': client_id,
            'annee': annee,
            'mois': mois,
            'status': status,
        },
    }
    
    return render(request, "views/depense_client.html", context)

@require_GET
@login_required(login_url='login_user_page')
def facture_fournisseur_page(request):
    # Récupération des paramètres
    reference = request.GET.get('reference', '')
    fournisseur_id = request.GET.get('fournisseur', '')
    annee = request.GET.get('annee', '')
    mois = request.GET.get('mois', '')
    status = request.GET.get('status', '')
    
    # Liste des fournisseurs pour le filtre
    listeFournisseur = Company.objects.filter(is_supplier=True).values('id', 'name')
    
    # Construction des filtres avec Q
    if reference:
        conditions = Q(invoice_number__icontains=reference)
    else:
        conditions = Q()
        
        if fournisseur_id:
            conditions &= Q(company_id=fournisseur_id)
        if status:
            conditions &= Q(status=status)
        if annee and mois:
            conditions &= Q(invoice_date__year=annee, invoice_date__month=mois)
        elif annee:
            conditions &= Q(invoice_date__year=annee)
        elif mois:
            conditions &= Q(invoice_date__year=timezone.now().year, invoice_date__month=mois)
    
    # Application des filtres
    factures_list = Invoice.objects.filter(is_supplier=True).filter(conditions).order_by('-invoice_date')
    
    # Pagination
    paginator = Paginator(factures_list, 20)
    
    try:
        factures = paginator.page(request.GET.get('page', 1))
    except (EmptyPage, ValueError, TypeError):
        factures = paginator.page(1) if paginator.num_pages > 0 else []
    
    context = {
        'listeFournisseur': listeFournisseur,
        'months': MONTHS,
        'etats': ETAT,
        'factures': factures,
        'paginator': paginator,
        'page_vide': isinstance(factures, list),
        'filtres': {
            'reference': reference,
            'fournisseur': fournisseur_id,
            'annee': annee,
            'mois': mois,
            'status': status,
        },
    }
    
    return render(request, "views/depense_fournisseur.html", context)

@require_POST
@login_required(login_url='login_user_page')
def newFactureClient(request):
    client_id = request.POST.get('client')
    num_reference = request.POST.get('num_reference')
    date_facture = request.POST.get('date_facture')
    montant_facture = request.POST.get('montant_facture')
    date_paiement_prevu = request.POST.get('date_paiement_prevu')
    Invoice.objects.create(
        invoice_number=num_reference,
        invoice_date=date_facture,
        expected_payment_date=date_paiement_prevu,
        total_amount=montant_facture,
        paid_amount=0,
        status=2,
        company=Company(client_id),
        is_supplier=False
    )
    return redirect('facture_client_page')

@require_POST
@login_required(login_url='login_user_page')
def newFactureFournisseur(request):
    fournisseur_id = request.POST.get('fournisseur')
    num_reference = request.POST.get('num_reference')
    date_facture = request.POST.get('date_facture')
    montant_facture = request.POST.get('montant_facture')
    date_paiement_prevu = request.POST.get('date_paiement_prevu')
    Invoice.objects.create(
        invoice_number=num_reference,
        invoice_date=date_facture,
        expected_payment_date=date_paiement_prevu,
        total_amount=montant_facture,
        paid_amount=0,
        status=2,
        company=Company(fournisseur_id),
        is_supplier=True
    )
    return redirect('facture_fournisseur_page')

@require_POST
@login_required(login_url='login_user_page')
def new_paiement_client(request):
    payment_date = datetime.strptime(request.POST.get('date_paiement'), '%Y-%m-%d').date()
    invoice = Invoice.objects.get(id=request.POST.get('facture_id'))
    status=request.POST.get('status', '')
    if not status :
        status=3 if invoice.expected_payment_date<payment_date else 2
    Payment.objects.create(
        amount=invoice.total_amount,
        payment_date=payment_date,
        invoice=invoice,
    )
    Invoice.objects.filter(id=invoice.id).update(
        actual_payment_date=payment_date,
        paid_amount=invoice.paid_amount + float(invoice.total_amount),
        status=status
    )
    return redirect('facture_client_page')

@require_POST
@login_required(login_url='login_user_page')
def new_paiement_fournisseur(request):
    payment_date = datetime.strptime(request.POST.get('date_paiement'), '%Y-%m-%d').date()
    invoice = Invoice.objects.get(id=request.POST.get('facture_id'))
    status=request.POST.get('status', '')
    if not status :
        status=3 if invoice.expected_payment_date<payment_date else 2
    Payment.objects.create(
        amount=invoice.total_amount,
        payment_date=payment_date,
        invoice=invoice,
    )
    Invoice.objects.filter(id=invoice.id).update(
        actual_payment_date=payment_date,
        paid_amount=invoice.paid_amount + float(invoice.total_amount),
        status=status
    )
    return redirect('facture_fournisseur_page')