# views.py
from django.contrib import messages

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from Constantes import ETAT, MONTHS
from tresorerie.metier.Company import Company
from django.core.paginator import Paginator, EmptyPage
from tresorerie.metier.FinancialTransaction import FinancialTransaction
from tresorerie.metier.Invoice import Invoice
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError
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
    try:
        payment_date = datetime.strptime(request.POST.get('date_paiement'), '%Y-%m-%d').date()
        invoice = Invoice.objects.get(id=request.POST.get('facture_id'))
        status = request.POST.get('status', '')
        
        payment = Payment(
            amount=invoice.total_amount,
            payment_date=payment_date,
            invoice=invoice
        )
        payment.save(user=request.user, status=status)
        
        messages.success(request, "Paiement client enregistré avec succès")
        
    except Invoice.DoesNotExist:
        messages.error(request, "Facture introuvable")
    except ValidationError as e:
        messages.error(request, str(e.messages[0]))
    except Exception as e:
        messages.error(request, f"Erreur inattendue : {str(e)}")
    
    return redirect('facture_client_page')

@require_POST
@login_required(login_url='login_user_page')
def new_paiement_fournisseur(request):
    try:
        payment_date = datetime.strptime(request.POST.get('date_paiement'), '%Y-%m-%d').date()
        invoice = Invoice.objects.get(id=request.POST.get('facture_id'))
        status = request.POST.get('status', '')
        
        payment = Payment(
            amount=invoice.total_amount,
            payment_date=payment_date,
            invoice=invoice
        )
        payment.save(user=request.user, status=status)
        
        messages.success(request, "Paiement fournisseur enregistré avec succès")
        
    except Invoice.DoesNotExist:
        messages.error(request, "Facture introuvable")
    except ValidationError as e:
        messages.error(request, str(e.messages[0]))
    except Exception as e:
        messages.error(request, f"Erreur inattendue : {str(e)}")
    
    return redirect('facture_fournisseur_page')

@require_GET
@login_required(login_url='login_user_page')
def mouvement_argent_page(request):
    # Récupération des paramètres de recherche
    transaction_number = request.GET.get('num_reference', '')
    transaction_date = request.GET.get('date_mouvement', '')
    transaction_type = request.GET.get('transaction_type', '')  # 'inflow', 'outflow', ou vide
    
    # Construction des filtres avec Q
    filters = Q()
    
    if transaction_number:
        filters &= Q(id__icontains=transaction_number)  # Recherche par ID (transaction_number)
    
    if transaction_date:
        filters &= Q(transaction_date=transaction_date)  # Recherche exacte par date
    
    if transaction_type == '1':
        filters &= Q(cash_inflow__gt=0)  # Transactions avec entrée d'argent
    elif transaction_type == '2':
        filters &= Q(cash_outflow__gt=0)  # Transactions avec sortie d'argent
    
    # Récupération des transactions avec filtres appliqués
    mouvements_list = FinancialTransaction.objects.filter(filters).order_by('-transaction_date')
    
    # Pagination
    paginator = Paginator(mouvements_list, 20)
    
    try:
        mouvements = paginator.page(request.GET.get('page', 1))
    except (EmptyPage, ValueError, TypeError):
        mouvements = paginator.page(1) if paginator.num_pages > 0 else []
    
    # Types de transactions pour le select dans le template
    transaction_types = [
        {'value': '', 'label': 'Tous les types'},
        {'value': 'inflow', 'label': 'Entrées (cash inflow)'},
        {'value': 'outflow', 'label': 'Sorties (cash outflow)'},
    ]
    
    context = {
        'mouvements': mouvements,
        'page_vide': isinstance(mouvements, list),
        'transaction_types': transaction_types,
        # Pour préserver les valeurs des filtres dans le template
        'search_filters': {
            'transaction_number': transaction_number,
            'transaction_date': transaction_date,
            'transaction_type': transaction_type,
        }
    }
    
    return render(request, "views/mouvement_argent.html", context)

@require_POST
@login_required(login_url='login_user_page')
def new_mouvement_argent(request):
    try:
        # Récupération des données
        transaction_number = request.POST.get('num_reference')
        montant = float(request.POST.get('montant'))
        transaction_date = datetime.strptime(request.POST.get('date_transaction'), '%Y-%m-%d').date()
        description = request.POST.get('description')
        type_transaction = request.POST.get('type_transaction')
        
        # Détermination du type de flux
        if type_transaction == "1":  # Attention : type_transaction est une string
            cash_inflow = montant
            cash_outflow = 0.0
        else:
            cash_inflow = 0.0
            cash_outflow = montant
        
        # Création de l'objet (la validation se fait dans save())
        transaction = FinancialTransaction(
            transaction_number=transaction_number,
            cash_inflow=cash_inflow,
            cash_outflow=cash_outflow,
            transaction_date=transaction_date,
            description=description,
            user=request.user
        )
        
        # Sauvegarde avec validation automatique
        transaction.save()
        
        messages.success(request, "Mouvement créé avec succès")
        
    except ValidationError as e:
        # Capture les erreurs de validation (dont le stock insuffisant)
        messages.error(request, str(e.messages[0]))
    except ValueError as e:
        messages.error(request, f"Erreur de format : {str(e)}")
    except Exception as e:
        messages.error(request, f"Erreur inattendue : {str(e)}")
    
    return redirect('mouvement_argent_page')