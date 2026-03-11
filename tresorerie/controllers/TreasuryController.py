# views.py
import json

from django.contrib import messages

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from Constantes import ETAT, MONTHS
from tresorerie.metier.Company import Company
from django.core.paginator import Paginator, EmptyPage
from tresorerie.metier.FinancialTransaction import FinancialTransaction
from tresorerie.metier.Invoice import Invoice
from datetime import datetime
from django.db.models import Q, FloatField, Sum, Value
from django.utils import timezone
from django.core.exceptions import ValidationError
from tresorerie.metier.Payment import Payment
from django.db.models.functions import Coalesce

@require_GET
@login_required(login_url='login_user_page') 
def tresorerie_page(request):
    solde_actualise = FinancialTransaction.objects.aggregate(
        solde=(
            Coalesce(Sum('cash_inflow'), Value(0), output_field=FloatField()) - 
            Coalesce(Sum('cash_outflow'), Value(0), output_field=FloatField())
        )
    )['solde']
    return render(request, "views/tresorerie.html", {'solde_actualise': solde_actualise})

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

@require_GET
@login_required(login_url='login_user_page')
def facture_regler_page(request):
    # Récupération de toutes les factures
    factures_list = Invoice.objects.all().exclude(status=2).order_by('-invoice_date')
    
    reference_list=Invoice.objects.filter(status=2).values('id', 'invoice_number', 'total_amount', 'is_supplier')
    
    solde_depart = FinancialTransaction.objects.filter(
        cash_outflow=0,
        cash_inflow__gt=0
    ).order_by('transaction_date', 'id').values_list('cash_inflow', flat=True).first()
    
    solde_actualise = FinancialTransaction.objects.aggregate(
        solde=(
            Coalesce(Sum('cash_inflow'), Value(0), output_field=FloatField()) - 
            Coalesce(Sum('cash_outflow'), Value(0), output_field=FloatField())
        )
    )['solde']
    
    # Séparer les factures par type
    factures_client = list(factures_list.filter(is_supplier=False).order_by('-invoice_date'))
    factures_fournisseur = list(factures_list.filter(is_supplier=True).order_by('-invoice_date'))
    autre_transaction_fournisseur= FinancialTransaction.objects.filter(from_invoice=False, cash_outflow__gt=0).order_by('-transaction_date')
    autre_transaction_client= FinancialTransaction.objects.filter(from_invoice=False, cash_inflow__gt=0).order_by('-transaction_date')
    
    # Créer des paires pour l'affichage côte à côte
    factures_pairees = []
    max_len = max(len(factures_client), len(factures_fournisseur))
    
    for i in range(max_len):
        facture_client = factures_client[i] if i < len(factures_client) else None
        facture_fournisseur = factures_fournisseur[i] if i < len(factures_fournisseur) else None
        factures_pairees.append({
            'client': facture_client,
            'fournisseur': facture_fournisseur,
        })
        
    max_len = max(len(autre_transaction_fournisseur), len(autre_transaction_client))
    
    for i in range(max_len):
        transaction_fournisseur = Invoice(
                                    invoice_number=autre_transaction_fournisseur[i].transaction_number, 
                                    invoice_date=autre_transaction_fournisseur[i].transaction_date, 
                                    total_amount=autre_transaction_fournisseur[i].cash_outflow
                                ) if i < len(autre_transaction_fournisseur) else None
        transaction_client = Invoice(
                                    invoice_number=autre_transaction_client[i].transaction_number,
                                    invoice_date=autre_transaction_client[i].transaction_date,
                                    total_amount=autre_transaction_client[i].cash_inflow
                                ) if i < len(autre_transaction_client) else None
        factures_pairees.append({
            'client': transaction_client,
            'fournisseur': transaction_fournisseur,
        })
        
        
    
    # Calculer les totaux pour TOUTES les factures (pas seulement la page courante)
    total_client = sum(
        paire['client'].total_amount 
        for paire in factures_pairees 
        if paire['client'] is not None
    )

    total_fournisseur = sum(
        paire['fournisseur'].total_amount 
        for paire in factures_pairees 
        if paire['fournisseur'] is not None
    )

    
    # Pagination
    paginator = Paginator(factures_pairees, 20)
    page_number = request.GET.get('page', 1)
    
    try:
        factures = paginator.page(page_number)
    except (EmptyPage, ValueError, TypeError):
        factures = paginator.page(paginator.num_pages) if paginator.num_pages > 0 else paginator.page(1)
    
    context = {
        'factures': factures,
        'page_vide': factures.paginator.count == 0,
        'total_fournisseur': total_fournisseur,
        'total_client': total_client,
        'solde_depart': solde_depart,
        'solde_actualise': solde_actualise,
        'reference_list': reference_list,
    }
    
    return render(request, "views/facture_regler.html", context)

@require_GET
@login_required(login_url='login_user_page')
def get_solde_actuel(request):
    """API qui retourne le solde actualisé"""
    try:
        solde_actualise = FinancialTransaction.objects.aggregate(
            solde=(
                Coalesce(Sum('cash_inflow'), Value(0), output_field=FloatField()) - 
                Coalesce(Sum('cash_outflow'), Value(0), output_field=FloatField())
            )
        )['solde']
        
        return JsonResponse({
            'success': True,
            'solde': float(solde_actualise)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
        
@require_POST
@login_required(login_url='login_user_page') 
def new_paiements(request):
    data = json.loads(request.body)
    listeSend=data.get('listSend', [])
    print(listeSend)
    for item in listeSend:
        id = item.get('id')
        date_paiement = item.get('date_paiement')
        
        try:
            invoice = Invoice.objects.get(id=id)
            payment_date = datetime.strptime(date_paiement, '%Y-%m-%d').date()
            
            payment = Payment(
                amount=invoice.total_amount,
                payment_date=payment_date,
                invoice=invoice
            )
            payment.save(user=request.user, status='') 
        except Invoice.DoesNotExist:
            messages.error(request, "Facture introuvable")
        except ValidationError as e:
            messages.error(request, str(e.messages[0]))
        except Exception as e:
            messages.error(request, f"Erreur inattendue : {str(e)}")

    return JsonResponse({'success': True})