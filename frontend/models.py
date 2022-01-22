from django.db import models
import os
# Create your models here.
from django.contrib.auth.models import AbstractUser 


def content_file_user(instance, filename):
    return 'profile/{1}'.format(instance, filename)

def loan_attach_file(instance, filename):
    return 'loan_attach/{1}'.format(instance, filename)

class User(AbstractUser):
    picture = models.ImageField(upload_to=content_file_user, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    id_num = models.IntegerField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    ### 0 : Regular User, 1 : Company User
    role = models.IntegerField(null=True, blank=True, default=0)
    company = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.username
    class Meta:
        permissions = (("admin_user","Can use modules admin"),("guest_user","Can use modules guest"))

class City(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class WorkIndustry(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Purpose(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class IncomeProof(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class IncomeType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class LoanSecurity(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Currency(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    
class Loan(models.Model):
    header = models.TextField(blank=True)
    purpose = models.ForeignKey('Purpose', on_delete=models.SET_NULL, blank=True, null=True)
    loan_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    loan_term = models.IntegerField(null=True, blank=True, default=0)
    loan_security = models.ForeignKey('LoanSecurity', on_delete=models.SET_NULL, blank=True, null=True)
    co_borrower = models.CharField(max_length=60, blank=True, null=True)
    income_type = models.ForeignKey('IncomeType', on_delete=models.SET_NULL, blank=True, null=True)
    income_proof = models.ForeignKey('IncomeProof', on_delete=models.SET_NULL, blank=True, null=True)
    income_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    payable_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    dependents = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, blank=True, null=True)
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    industry = models.ForeignKey('WorkIndustry', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    ### 0 : Pending, 1 : Declined, 2 : Active, 3: Pending, 4 : Completed
    status = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.header

class LoanAttach(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to=loan_attach_file, blank=True, null=True)
    
    def __str__(self):
        return os.path.basename(self.file.name)
    
    def delete(self):
        self.file.delete()
        super(LoanAttach, self).delete()    

class LoanBid(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, blank=True, null=True)
    borrow_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    borrow_term = models.IntegerField(null=True, blank=True, default=0)
    issuance_fee = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    loan_rate = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    effective_rate = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    monthly_payable = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    total_payable = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    ### 0 : Bid, 1 : Revoked, 2 : Awarded, 3 : Completed
    status = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    awarded_at = models.DateTimeField(blank=True, null=True)
    revoked_at = models.DateTimeField(blank=True, null=True)

class Comment(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    msg = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']