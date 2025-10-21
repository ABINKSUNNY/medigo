from django.urls import path
from . import views
urlpatterns =[

    path('adminmanage_patient/', views.adminmanage_patient, name='admin_manage_patient'),

    path('reg_patient/', views.reg_patient, name='reg_patient'),

    path('patientview/',views.patientview,name='view_patient'),

    path('delete_patient/<int:idd>/', views.delete, name='dele'),


    path('profile_view/',views.editview,name='edit'),

    path('patient_edit/<int:idd>/', views.patient_edit, name='patient_edit'),

]