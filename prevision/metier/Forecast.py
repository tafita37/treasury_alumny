from django.db import models

class Forecast(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    months = models.SmallIntegerField(db_column='months')
    years = models.IntegerField(db_column='years')
    cash_inflow = models.IntegerField(db_column='cash_inflow')
    cash_outflow = models.IntegerField(db_column='cash_outflow')

    class Meta:
        db_table = 'forecast'