from django.urls import path
from . import views
urlpatterns = [

    path('add_pres/',views.add_pres,name='add_pres'),
    path('view_pres/', views.view_pres, name='view_pres'),
    path('download_prescription/<int:pres_id>/', views.download_prescription, name='download_prescription'),


]