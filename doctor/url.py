from django.urls import path

from . import views
urlpatterns =[
    path('adminview_doc/',views.adminview_doc,name='adminview_doc'),

    path('hospitalview_doc/',views.hospitalview_doc,name='hospitalview_doc'),

    path('reg_doc/',views.reg_doc,name='reg_doc'),

    path('approve/<str:idd>/', views.approve, name='approve'),
    path('reject/<str:idd>/', views.reject, name='reject'),
    path('delete/<str:idd>/', views.delete, name='delete'),


]