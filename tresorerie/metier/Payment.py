from django.db import models

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

    class Meta:
        db_table = "payment"

    def __str__(self):
        return self.payment_number
