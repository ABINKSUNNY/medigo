from django.shortcuts import render
from pharmacy.models import *
from login.models import Login
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from cart.models import Purchase

# Create your views here.
def admin_managepha(request):
    obj=Pharmacy.objects.filter(status="pending")
    context = {
        'obj':obj,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'pharmacy/admin_managepha.html',context)

# def reg_pha(request):
#     if request.method == "POST":
#         obj=Pharmacy()
#         obj.name = request.POST.get('name')
#         obj.place = request.POST.get('place')
#         obj.address = request.POST.get('address')
#         obj.contact = request.POST.get('contact')
#         obj.email = request.POST.get('email')
#         myfile = request.FILES["licence"]
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         obj.licence = myfile.name
#         obj.status = 'pending'
#
#         obj.password=request.POST.get('password')
#         obj.repass=request.POST.get('repass')
#         obj.save()
#
#         objlist = "Pharmacy Registered Successfully.."
#         context = {
#             'msg': objlist
#         }
#         return render(request, 'pharmacy/reg_pha.html',context)
#     return render(request,'pharmacy/reg_pha.html')
def reg_pha(request):
    if request.method == "POST":
        name = request.POST.get('name')
        place = request.POST.get('place')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repass = request.POST.get('repass')
        licence_file = request.FILES.get("licence")

        # Validation checks
        if not all([name, place, address, contact, email, password, repass, licence_file]):
            return render(request, 'pharmacy/reg_pha.html', {'error': 'All fields are required.'})

        if not contact.isdigit() or len(contact) != 10:
            return render(request, 'pharmacy/reg_pha.html', {'error': 'Phone number must be exactly 10 digits.'})

        # 🚫 Password minimum length validation
        if len(password) < 6:
            return render(request, 'pharmacy/reg_pha.html', {'error': 'Password must be at least 6 characters long.'})

        if password != repass:
            return render(request, 'pharmacy/reg_pha.html', {'error': 'Passwords do not match.'})

        if Login.objects.filter(username=email).exists():
            return render(request, 'pharmacy/reg_pha.html', {'error': 'Email already registered.'})

        # Save file
        fs = FileSystemStorage()
        filename = fs.save(licence_file.name, licence_file)

        # Save Pharmacy
        pharmacy = Pharmacy(
            name=name,
            place=place,
            address=address,
            contact=contact,
            email=email,
            licence=filename,
            status='pending',
            password=password,
            repass=repass
        )
        pharmacy.save()

        # # Save Login entry (optional)
        # login = Login(
        #     username=email,
        #     password=password,
        #     type='pharmacy',
        #     u_id=pharmacy.pha_id  # Adjust field if needed
        # )
        # login.save()

        return render(request, 'pharmacy/reg_pha.html', {'msg': 'Pharmacy Registered Successfully.'})

    return render(request, 'pharmacy/reg_pha.html')

def view_pha(request):

    obj=Pharmacy.objects.all()
    context = {
        'obj':obj
    }
    return render(request,'pharmacy/view_pha.html',context)

def admin_viewpha(request):
    obj=Pharmacy.objects.all()
    context = {
        'obj':obj,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'pharmacy/admin_viewpha.html',context)


def approve_pha(request,idd):
    obj=Pharmacy.objects.get(pha_id=idd)
    obj.status="approved"
    obj.save()
    ob = Login()
    ob.username = obj.email
    ob.password = obj.password
    ob.type = 'pharmacy'
    ob.u_id = obj.pha_id
    ob.save()
    return admin_managepha(request)



def reject_pha(request,idd):
    obj=Pharmacy.objects.get(pha_id=idd)
    obj.status="rejected"
    obj.save()
    return admin_managepha(request)

def de(request,idd):
    obj=Pharmacy.objects.get(pha_id=idd).delete()
    return admin_viewpha(request)

def ppayment(request):
    pharmacy = request.session.get("uid")
    obj = Purchase.objects.filter(pharmacy_id=pharmacy)
    context ={

        'cd':obj
    }
    return render(request,"pharmacy/ppayment.html",context)

