
from django.shortcuts import render, get_object_or_404,redirect
from delivery.models import Delivery
from deliveryagent.models import Deliveryagent
from cart.models import Purchase
from django.urls import reverse

def phaview_status(request):
    dd = request.session["uid"]
    obj=Delivery.objects.filter(pha_id=dd)
    context = {
        'cb':obj
    }
    return render(request,'delivery/phaview_delstatus.html', context)

def userview_status(request):
    dd = request.session["uid"]
    obj=Delivery.objects.filter(p_id=dd)
    context = {
        'cb':obj
    }
    return render(request,'delivery/userview_delstatus.html',context)

def update_del(request):
    dd = request.session["uid"]
    obj=Delivery.objects.filter(deliveryagent_id=dd)
    context = {
        'cb':obj
    }
    return render(request,'delivery/updatedelivery_status.html',context)

def deli_ss(request,idd):
    obj=Delivery.objects.get(de_id=idd)
    obj.status = "delivered"
    obj.save()
    return update_del(request)



def order(request):
    ord = request.session["uid"]
    obj=Purchase.objects.filter(pharmacy_id=ord,status='pending')
    context ={

        'obj':obj,
    }
    # return redirect(order)
    return render(request, 'delivery/order.html', context)


def assign_and_update_status(request, idd):
    try:
        obj = Purchase.objects.get(pu_id=idd)
        obj.status = 'assigned'
        obj.save()

        # Redirect to the assign view with pu_id in query string
        return redirect(f"{reverse('assign')}?pu_id={idd}")
    except Purchase.DoesNotExist:
        return redirect('order')

