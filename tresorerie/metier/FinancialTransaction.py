from django.db import models

from authentification.metier.User import User  # Assurez-vous que le chemin d'import est correct
from django.db.models import Sum
from django.core.exceptions import ValidationError

class FinancialTransaction(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    transaction_number = models.CharField(max_length=50, unique=True)
    cash_inflow = models.FloatField(db_column='cash_inflow')  # REAL en SQL = FloatField en Django
    cash_outflow = models.FloatField(db_column='cash_outflow')  # DOUBLE PRECISION = FloatField
    transaction_date = models.DateField(db_column='transaction_date')
    description = models.TextField(db_column='description')
    
    def save(self, *args, **kwargs):
        # Logique avant sauvegarde
        if self.cash_outflow > 0:
            # Vérifier le stock avant la date
            total_entrees = FinancialTransaction.objects.filter(
                transaction_date__lte=self.transaction_date
            ).aggregate(total=Sum('cash_inflow'))['total'] or 0
            
            total_sorties = FinancialTransaction.objects.filter(
                transaction_date__lte=self.transaction_date
            ).aggregate(total=Sum('cash_outflow'))['total'] or 0
            
            # Si c'est une modification, exclure cette transaction
            if self.pk:
                ancienne = FinancialTransaction.objects.get(pk=self.pk)
                total_sorties -= ancienne.cash_outflow
            
            stock_disponible = total_entrees - total_sorties
            
            if self.cash_outflow > stock_disponible:
                raise ValidationError(
                    f"Stock insuffisant ! Disponible: {stock_disponible} €"
                )
        
        # Appel à la méthode save originale
        super().save(*args, **kwargs)
    
    # Relation avec la table users
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )

    class Meta:
        db_table = 'financial_transaction'
        verbose_name = 'Financial Transaction'
        verbose_name_plural = 'Financial Transactions'

    def __str__(self):
        return f"Transaction {self.id} - {self.transaction_date}"