from django.urls import path

from . import views
urlpatterns =[


    path('pharmacyview_med/', views.pharmacyview_med, name='pharmacyview_med'),

    path('userview_med/', views.userview_med, name='userview_med'),

    path('del_med/<str:idd>/', views.del_med, name='deletemed'),


    path('userview_medall/', views.userview_medall, name='userview_medall'),

]