from django.urls import path

import appointment
from . import views
urlpatterns = [
    path('manageappointment/',views.manageappointment,name='manageappointment'),

    path('userapp/',views.user_app,name='userapp'),

    path('viewapp/',views.view_app,name='viewapp'),

    path('patientview/',views.patientview_app,name='patientapp'),
    path('hpayment/',views.hpayment,name='hpayment'),

    path('doc_view/',views.docview_app,name='docview_app'),
    path('chat/<str:idd>/',views.chat,name='chat'),

    path('approve/<str:idd>/', views.approve_app, name='appr'),
    path('reject/<str:idd>/', views.reject_app, name='rej'),
    path('cancel_apppat/<str:a_id>/',views.cancel_appointment,name='cancel_apppat'),
    path('cancel_apphos/<str:a_id>/',views.cancel_appointmenthos,name='cancel_apphos'),



    path('pay-now/<int:a_id>/', views.pay_now, name='pay_now'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),




]
