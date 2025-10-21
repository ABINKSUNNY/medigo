from django.shortcuts import render
from cart.models import *


def pharmacyview_med(request):
    pharmacy = request.session.get("uid")
    obj = Product.objects.filter(pharmacy_id=pharmacy)
    context = {
        'obj':obj
    }
    return render(request,'medicine/pharmacyview_med.html',context)

def userview_med(request):
    obj = Product.objects.all()
    context = {
        'obj':obj
    }
    return render(request,'medicine/userview_med.html',context)

def del_med(request,idd):
    obj = Product.objects.get(id=idd).delete()
    return pharmacyview_med(request)

def userview_medall(request):
    obj = Product.objects.all()
    context = {
        'obj':obj
    }
    return render(request,'medicine/userview_medall.html',context)