from django.urls import path
from temp import views
urlpatterns = [
    path('index/',views.index,name='index'),

    path('admin_home/',views.admin_home,name='admin_home'),

    path('deliveryagent_home/',views.deliveryagent_home,name='deliveryagent_home'),

    path('doc_home/',views.doc_home,name='doc_home'),

    path('hospital_home/',views.hospital_home,name='hospital_home'),

    path('patient_home/',views.patient_home,name='patient_home'),

    path('pharmacy_home/',views.pharmacy_home,name='pharmacy_home'),
]