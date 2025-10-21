from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    # path('products/(?P<idd>\w+)', views.view_products, name='view_products'),
    path('products/<str:idd>/', views.view_products, name='view_products'),

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('complete_payment/', views.complete_payment, name='complete_payment'),
    path('add_product/',views.add_product,name='add_product'),
    path('medall/',views.medall,name='medall')
]
