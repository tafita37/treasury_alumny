from django.db import models, transaction
from django.core.exceptions import ValidationError
from datetime import datetime
from tresorerie.metier.FinancialTransaction import FinancialTransaction
from tresorerie.metier.Invoice import Invoice

class Payment(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    payment_number = models.CharField(max_length=50, unique=True)
    amount = models.FloatField()
    payment_date = models.DateField()

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        db_column="invoice_id"
    )
    
    def save(self, *args, **kwargs):
        # Vérifier si c'est une création ou une modification
        is_new = self.pk is None
        user = kwargs.pop('user', None)
        status = kwargs.pop('status', None)
        
        with transaction.atomic():
            if is_new:
                # Récupérer la facture associée
                invoice = self.invoice
                
                status = 3 if invoice.expected_payment_date < self.payment_date else 1
                # Déterminer le type de transaction en fonction de is_supplier
                if invoice.is_supplier:
                    # C'est une facture fournisseur → Décaissement (sortie d'argent)
                    cash_outflow = self.amount
                    cash_inflow = 0.0
                    description = f"Paiement fournisseur - Facture {invoice.invoice_number}"
                else:
                    # C'est une facture client → Encaissement (entrée d'argent)
                    cash_outflow = 0.0
                    cash_inflow = self.amount
                    description = f"Paiement client - Facture {invoice.invoice_number}"
                
                try:
                    # Créer la transaction financière
                    FinancialTransaction.objects.create(
                        cash_inflow=cash_inflow,
                        cash_outflow=cash_outflow,
                        transaction_date=self.payment_date,
                        description=description,
                        user=user,
                        from_invoice=True  # Indiquer que cette transaction provient d'une facture
                        # Ajustez selon votre modèle User
                    )
                    
                    Invoice.objects.filter(id=invoice.id).update(
                        actual_payment_date=self.payment_date,
                        paid_amount=self.amount,
                        status=status
                    )
                except ValidationError as e:
                    # Si la validation de stock échoue (pour les décaissements)
                    raise ValidationError(f"Erreur: {str(e.messages[0])}")
                
                # Sauvegarder le paiement
                super().save(*args, **kwargs)
                
            else:
                # C'est une modification d'un paiement existant
                # Logique pour les modifications si nécessaire
                super().save(*args, **kwargs)

    class Meta:
        db_table = "payment"

    def __str__(self):
        return self.payment_number
