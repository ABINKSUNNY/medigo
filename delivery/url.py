from django.urls import path
from . import views
urlpatterns =[



path('phaview_del/',views.phaview_status,name='phaview_del'),

path('userview_del/',views.userview_status,name='userview_del'),

path('update_del/',views.update_del,name='update_del'),

path('del_s/<str:idd>/',views.deli_ss, name='delstatus'),

path('order/',views.order,name='order'),

# path('delivery/status/<str:idd>/', views.status, name='status'),

path('assign_status/<str:idd>/', views.assign_and_update_status, name='assign_status'),
# path('assign/<int:order_id>/', views.assign, name='assign'),




]