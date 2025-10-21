from django.urls import path


from . import views
urlpatterns = [
    path('login/', views.login, name='login'),
    path('forgot_password/', views.forgot_password_request, name='forgot_password_request'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
]