"""
URL configuration for medigo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from temp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',include('login.url')),
    path('hospital/',include('hospital.url')),
    path('patient/',include('patient.url')),
    path('doctor/',include('doctor.url')),
    path('pharmacy/',include('pharmacy.url')),
    path('deliveryagent/',include('deliveryagent.url')),
    path('delivery/',include('delivery.url')),
    path('payment/',include('payment.url')),
    path('prescription/',include('prescription.url')),
    path('complaint/',include('complaint.url')),
    path('chat/',include('chat.url')),
    path('cart/',include('cart.url')),
    path('appointment/',include('appointment.url')),
    path('medicine/',include('medicine.url')),
    path('temp/',include('temp.url')),
    path('',views.index)



]


# ✅ Add this to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)