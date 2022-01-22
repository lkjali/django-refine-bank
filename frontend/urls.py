from django.urls import path
from django.conf.urls import url

from django.contrib.auth.views import PasswordResetView 
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView

from .views import *

urlpatterns = [
	url(r'^$', index, name='index'),

	# auth part
	url(r'^login', LoginView.as_view(), name='login'),
	url(r'^logout', LogoutView.as_view(), name='logout'),
	url(r'^signup', register, name='signup'),
	url(r'^profile/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile'),
	url(r'^ajax-reset-user/$', ajax_reset_user, name='ajax-reset-user'),

	url(r'^test', Test.as_view(), name='test'),
	url(r'^reset/password/$', PasswordResetView.as_view(template_name='password_reset_form.html', email_template_name='password_reset_email.html'), name='password_reset'),
    url(r'^reset/password/reset/done/$', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
	# loan part
	url(r'^create-loan', LoanAdd.as_view(), name='create-loan'),
	url(r'^update-loan/(?P<pk>\d+)/$', LoanUpdate.as_view(), name='update-loan'),
	url(r'^ajax-delete-loan/$', ajax_delete_loan, name='ajax-delete-loan'),
	url(r'^ajax-delete-loan-attach/$', ajax_delete_loan_attach, name='ajax-delete-loan-attach'),

	url(r'^detail-loan/(?P<pk>\d+)/$', LoanDetail.as_view(), name='detail-loan'),

	url(r'^loans', Loans.as_view(), name='loans'),

	# bid part
	url(r'^make-loan-bid/$', make_loan_bid, name='make-loan-bid'),
	url(r'^ajax-award-bid/$', ajax_award_bid, name='ajax-award-bid'),
	url(r'^ajax-revoke-bid/$', ajax_revoke_bid, name='ajax-revoke-bid'),
	url(r'^ajax-accept-award/$', ajax_accept_award, name='ajax-accept-award'),
	url(r'^ajax-reject-award/$', ajax_reject_award, name='ajax-reject-award'),

	# comment part
	url(r'^ajax-add-comment/$', ajax_add_comment, name='ajax-add-comment'),
	url(r'^ajax-delete-comment/$', ajax_delete_comment, name='ajax-delete-comment'),

	# admin part
	url(r'^users', Users.as_view(), name='users'),
	url(r'^ajax-change-role/$', ajax_change_role, name='ajax-change-role'),
	url(r'^ajax-delete-user/$', ajax_delete_user, name='ajax-delete-user'),

	url(r'^pending-loans', PendingLoans.as_view(), name='pending-loans'),
	url(r'^ajax-accept-loan/$', ajax_accept_loan, name='ajax-accept-loan'),
	url(r'^ajax-decline-loan/$', ajax_decline_loan, name='ajax-decline-loan'),
	
]