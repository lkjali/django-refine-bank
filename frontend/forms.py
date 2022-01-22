from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'id_num', 'birthday', 'email', 'picture', 'username')

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ('header', 'purpose', 'loan_amount', 'loan_term', 'loan_security', 'co_borrower', 'income_type', 'income_proof', 
         'income_amount', 'payable_amount', 'marital_status', 'dependents', 'city', 'currency', 'address', 'industry', 'user')

