from django.urls import path
from . import views
from .views import reg_pha

urlpatterns = [

    path('admin_managepha/', views.admin_managepha, name='admin_managepha'),
    path('reg_pha/', views.reg_pha, name='reg_pha'),
    path('view_pha/', views.view_pha, name='view_pha'),
    path('admin_viewpha/',views.admin_viewpha, name='admin_viewpha'),
    path('ppayment/',views.ppayment,name='ppayment'),

    path('approve_pha/<str:idd>/', views.approve_pha, name='ap'),
    path('reject_pha/<str:idd>/', views.reject_pha, name='re'),
    path('admin_viewpha/<str:idd>/', views.de, name='de'),

]