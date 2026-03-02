from django.db import models
from tresorerie.metier.CompanyType import CompanyType

class Company(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100, unique=True, db_column='name')
    registration_number = models.CharField(max_length=50, unique=True, db_column='registration_number')
    tax_identification_number = models.CharField(max_length=50, unique=True, db_column='tax_identification_number')
    email = models.CharField(max_length=50, unique=True, db_column='email')
    phone = models.CharField(max_length=50, unique=True, db_column='phone')
    address = models.CharField(max_length=50, unique=True, db_column='address')
    website_url = models.TextField(unique=True, db_column='website_url')
    created_at = models.DateField(db_column='created_at')
    is_supplier = models.BooleanField(db_column='is_supplier')
    
    company_type = models.ForeignKey(
        CompanyType,
        on_delete=models.CASCADE,
        db_column="company_type_id"
    )

    class Meta:
        db_table = "company"

    def __str__(self):
        return self.name