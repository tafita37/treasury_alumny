from django.db import models

class Invoice(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField()
    expected_payment_date = models.DateField()
    actual_payment_date = models.DateField(null=True, blank=True)

    total_amount = models.FloatField()
    paid_amount = models.FloatField()

    status = models.SmallIntegerField()

    company = models.ForeignKey(
        "Company",
        on_delete=models.PROTECT,
        db_column="company_id"
    )

    class Meta:
        db_table = "invoice"

    def __str__(self):
        return self.invoice_number