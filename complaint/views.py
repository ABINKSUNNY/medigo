from datetime import datetime

from django.shortcuts import render

from complaint.models import Complaint


# Create your views here.
def post_comp(request):
    comp=request.session["uid"]
    if request.method == 'POST':
        obj=Complaint()
        obj.p_id_id=comp
        obj.complaint=request.POST.get('complaint')
        obj.date=datetime.today()
        obj.time=datetime.today()
        obj.reply='pending'
        obj.save()

    return render(request,'complaint/postcomplaint.html')

def view_comp(request):
    obj=Complaint.objects.filter(reply="pending")
    context = {
        'cb':obj
    }
    return render(request,'complaint/viewcomplaint.html',context)


def post_reply(request,idd):
    obj=Complaint.objects.filter(c_id=idd)
    context = {
        'cb':obj
    }

    if request.method == 'POST':
        comp = request.session["uid"]
        obj=Complaint.objects.get(c_id=idd)
        obj.p_id=comp
        obj.reply=request.POST.get('reply')
        obj.date=datetime.today()
        obj.time=datetime.today()
        obj.save()
        return view_comp(request)

    return render(request,'complaint/postreply.html',context)

def viewreply(request):
    comp = request.session["uid"]
    obj = Complaint.objects.filter(patient_id=comp)
    context = {
        'cb': obj
    }
    return render(request,'complaint/viewreply.html',context)