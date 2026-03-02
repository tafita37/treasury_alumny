from django.db import models

class CompanyType(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=50, unique=True, db_column='name')

    class Meta:
        db_table = 'company_type'