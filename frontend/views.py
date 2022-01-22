from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import JsonResponse
from django.utils import translation
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, TemplateView
from django.views.generic import FormView, RedirectView, View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password

from .models import *
from .forms import *

from datetime import datetime
# Create your views here.
def index(request):
    ## Regular User
    if request.user.is_authenticated :
        if request.user.role == 0 :
            loans = Loan.objects.filter(user=request.user)
            
            if len(loans) >= 1:
                awarded_proposals = LoanBid.objects.filter(loan_id=loans[0].id, status__gte = 2)
                awarded_proposal = None
                if len(awarded_proposals) >= 1:
                    awarded_proposal = awarded_proposals[0]
                    proposals = LoanBid.objects.filter(loan_id=loans[0].id).exclude(id=awarded_proposal.id)
                else:
                    proposals = LoanBid.objects.filter(loan_id=loans[0].id)
                
                loans[0].attached_files = LoanAttach.objects.filter(loan_id=loans[0].id)
                loans[0].comments = Comment.objects.filter(loan_id=loans[0].id)
                return render(request, 'front/regular_index.html',
                    { 
                        "loan": loans[0], 
                        'proposals': proposals, 
                        'awarded_proposal': awarded_proposal, 
                        
                    })
            else:
                return HttpResponseRedirect(reverse('create-loan'))
        ## Company User
        else:
            return HttpResponseRedirect(reverse('loans'))
    else:
        return render(request, 'index.html')

class Test(ListView):
    model = User
    template_name = "loan_new.html"

##### Auth Part #####
class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    
    def get_success_url(self):
        return reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super(LoginView, self).form_valid(form)

class LogoutView(RedirectView):
    url = '/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
    
# Register Function
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_num = request.POST.get('id_num')
        birthday = request.POST.get('birthday')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        email_qs = User.objects.filter(email = email)
        phone_qs = User.objects.filter(username = phone)
        if email_qs.exists():
            return render(request, 'signup.html', {'errors': '1', 'first_name': first_name, 'last_name': last_name, 'id_num': id_num, 'birthday': birthday, 'phone': phone, 'email': email })
        if phone_qs.exists():
            return render(request, 'signup.html', {'errors': '2', 'first_name': first_name, 'last_name': last_name, 'id_num': id_num, 'birthday': birthday, 'phone': phone, 'email': email})
        
        password = make_password(password)
        user = User(
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = password,
            birthday = birthday,
            phone = phone,
            username = phone,
            id_num = id_num,
        )
        user.save()
        #login(request, user)
        return redirect('login')

    else:
        return render(request, 'signup.html',{})

@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    model = User
    form_class = UserForm
    template_name = "profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user1'] = User.objects.get(pk=self.kwargs.get('pk'))
        return context
    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

def ajax_reset_user(request):
    password = request.POST.get('password')
    old_password = request.POST.get('old_password')
    
    if request.user.check_password(old_password) is False:
        return JsonResponse({'err_code': '1'})
    else:
        request.user.set_password(password)
        request.user.save()
        login(request, request.user)
    
    return JsonResponse({'err_code': '2'})

##### For Regular User ####
@method_decorator(login_required, name='dispatch')
class LoanAdd(CreateView):
    model = Loan
    form_class = LoanForm
    template_name = "front/loan_new.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.all()
        context["industries"] = WorkIndustry.objects.all()
        context["purposes"] = Purpose.objects.all()
        context["proofs"] = IncomeProof.objects.all()
        context["income_types"] = IncomeType.objects.all()
        context["loan_securities"] = LoanSecurity.objects.all()
        context["currencies"] = Currency.objects.all()
        return context
    def get_success_url(self):
        loan_id = self.kwargs.get('pk')
        print(loan_id)
        uploaded_files = self.request.FILES.getlist('files')
        for tmp_file in uploaded_files:
            print(tmp_file)
            obj = LoanAttach(
                loan_id = loan_id,
                file = tmp_file
            )
            obj.save()
        return reverse('index')

@method_decorator(login_required, name='dispatch')
class LoanUpdate(UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = "front/loan_new.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.all()
        context["industries"] = WorkIndustry.objects.all()
        context["purposes"] = Purpose.objects.all()
        context["proofs"] = IncomeProof.objects.all()
        context["income_types"] = IncomeType.objects.all()
        context["loan_securities"] = LoanSecurity.objects.all()
        context["currencies"] = Currency.objects.all()

        loan = Loan.objects.get(pk=self.kwargs.get('pk'))
        loan.attached_files = LoanAttach.objects.filter(loan_id=loan.id)
        context['loan'] = loan
        return context
    def get_success_url(self):
        print("OKOKOKOK")
        loan_id = self.kwargs.get('pk')
        print(loan_id)
        uploaded_files = self.request.FILES.getlist('files')
        for tmp_file in uploaded_files:
            print(tmp_file)
            obj = LoanAttach(
                loan_id = loan_id,
                file = tmp_file
            )
            obj.save()
        return reverse('index')

def ajax_delete_loan(request):
    loan_id = request.POST.get('loan_id')
    Loan.objects.get(id=loan_id).delete()
    
    return JsonResponse({'err_code': '2'})

def ajax_delete_loan_attach(request):
    attach_id = request.POST.get('attach_id')
    LoanAttach.objects.get(id=attach_id).delete()
    
    return JsonResponse({'err_code': '2'})

def ajax_award_bid(request):
    bid_id = request.POST.get('bid_id')
    loan_bid = LoanBid.objects.get(id=bid_id)
    loan_bid.status = 2
    loan_bid.awarded_at = datetime.now()
    loan_bid.save()

    loan = Loan.objects.get(id=loan_bid.loan_id)
    loan.status = 3
    loan.save()

    return JsonResponse({'err_code': '2'})

def ajax_revoke_bid(request):
    bid_id = request.POST.get('bid_id')
    
    loan_bid = LoanBid.objects.get(id=bid_id)
    loan_bid.status = 1
    loan_bid.revoked_at = datetime.now()
    loan_bid.save()

    loan = Loan.objects.get(id=loan_bid.loan_id)
    loan.status = 2
    loan.save()
    return JsonResponse({'err_code': '2'})

def ajax_accept_award(request):
    loan_id = request.POST.get('loan_id')
    bid_id = request.POST.get('bid_id')

    loan_bid = LoanBid.objects.get(id=bid_id)
    loan_bid.status = 3
    loan_bid.save()

    loan = Loan.objects.get(id=loan_id)
    loan.status = 4
    loan.completed_at = datetime.now()
    loan.save()
    return JsonResponse({'err_code': '2'})

def ajax_reject_award(request):
    loan_id = request.POST.get('loan_id')
    bid_id = request.POST.get('bid_id')

    loan_bid = LoanBid.objects.get(id=bid_id)
    loan_bid.status = 0
    loan_bid.save()

    loan = Loan.objects.get(id=loan_id)
    loan.status = 2
    loan.completed_at = datetime.now()
    loan.save()
    return JsonResponse({'err_code': '2'})
##### For Company User #####
@method_decorator(login_required, name='dispatch')
class LoanDetail(TemplateView):
    model = Loan
    template_name = "front/loan_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loan = Loan.objects.get(pk=self.kwargs.get('pk'))
        loan_bid = LoanBid.objects.filter(loan_id=loan.id, user_id=self.request.user.id)
        loan.attached_files = LoanAttach.objects.filter(loan_id=loan.id)
        loan.comments = Comment.objects.filter(loan_id=loan.id)
        context['loan'] = loan
        if len(loan_bid) >= 1 :
            context['loanbid'] = loan_bid[0]
        return context

@method_decorator(login_required, name='dispatch')
class Loans(TemplateView):
    model = Loan
    template_name = "front/loans.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # awarded bids
        awarded_bids = LoanBid.objects.filter(status__gte=2, user__id=self.request.user.id).order_by('-loan__status', '-awarded_at')
        # can be bidded
        loans = Loan.objects.filter(status=2)
        for loan in loans:
            loan.bidded = LoanBid.objects.filter(loan_id=loan.id, user_id=self.request.user.id).count()
        context['loans'] = loans
        context['awarded_bids'] = awarded_bids
        return context

def make_loan_bid(request):
    if request.method == 'POST':
        borrow_amount = request.POST.get('borrow_amount')
        borrow_term = request.POST.get('borrow_term')
        issuance_fee = request.POST.get('issuance_fee')
        loan_rate = request.POST.get('loan_rate')
        effective_rate = request.POST.get('effective_rate')
        monthly_payable = request.POST.get('monthly_payable')
        total_payable = request.POST.get('total_payable')
        user_id = request.POST.get('user_id')
        loan_id = request.POST.get('loan_id')
        bid_id = request.POST.get('bid_id')
        print(borrow_amount)
        if bid_id == "-1":
            loan_bid = LoanBid(
                borrow_amount = borrow_amount,
                borrow_term = borrow_term,
                issuance_fee = issuance_fee,
                loan_rate = loan_rate,
                effective_rate = effective_rate,
                monthly_payable = monthly_payable,
                total_payable = total_payable,
                user_id = user_id,
                loan_id = loan_id,
            )
            loan_bid.save()
        else:
            loan_bid = LoanBid.objects.get(id=bid_id)
            
            loan_bid.borrow_amount = borrow_amount
            loan_bid.borrow_term = borrow_term
            loan_bid.issuance_fee = issuance_fee
            loan_bid.loan_rate = loan_rate
            loan_bid.effective_rate = effective_rate
            loan_bid.monthly_payable = monthly_payable
            loan_bid.total_payable = total_payable
            loan_bid.save()

        return redirect('index')

##### comment #####
def ajax_add_comment(request):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        loan_id = request.POST.get('loan_id')
        user_id = request.POST.get('user_id')
        obj = Comment(msg=msg, loan_id=loan_id, user_id=user_id)
        obj.save()
        return render(request, 'widgets/comment_widget.html', {'comment': obj})

def ajax_delete_comment(request):
    comment_id = request.POST.get('comment_id')
    Comment.objects.get(id=comment_id).delete()
    
    return JsonResponse({'err_code': '2'})
##### admin part #####
@method_decorator(login_required, name='dispatch')
class Users(TemplateView):
    model = User
    template_name = "admin/users.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

def ajax_change_role(request):
    user_id = request.POST.get('user_id')
    role = request.POST.get('role')
    company = request.POST.get('company')
    user = User.objects.get(id=user_id)
    user.role = role
    user.company = company
    user.save()
    
    return JsonResponse({'err_code': '2'})

def ajax_delete_user(request):
    user_id = request.POST.get('user_id')
    User.objects.get(id=user_id).delete()
    
    return JsonResponse({'err_code': '2'})
@method_decorator(login_required, name='dispatch')
class PendingLoans(TemplateView):
    model = Loan
    template_name = "admin/pending_loans.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loans'] = Loan.objects.filter(status=0)
        return context

def ajax_accept_loan(request):
    loan_id = request.POST.get('loan_id')
    loan = Loan.objects.get(id=loan_id)
    loan.status = 2
    loan.save()
    
    return JsonResponse({'err_code': '2'})

def ajax_decline_loan(request):
    loan_id = request.POST.get('loan_id')
    loan = Loan.objects.get(id=loan_id)
    loan.status = 1
    loan.save()
    
    return JsonResponse({'err_code': '2'})
##### end Admin part #####