from django.template.context_processors import request
from django.urls import path
from . import views
urlpatterns = [
    path('manage_hos/', views.manage_hos, name='manage_hos'),
    path('hos_reg/', views.hos_reg, name='hos_reg'),
    path('userview_hos/', views.userview_hos, name='userview_hos'),
    path('admin_viewhos/', views.admin_viewhos, name='admin_viewhos'),

    path('approve_hos/<str:idd>/', views.approve_hos, name='approv'),
    path('reject_hos/<str:idd>/', views.reject_hos, name='rejec'),
    path('adminviewhos/<str:idd>/', views.delete, name='delet'),

]