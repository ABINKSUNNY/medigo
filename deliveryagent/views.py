from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from deliveryagent.models import *
from login.models import Login
from delivery.models import Delivery
import datetime
from cart.models import Purchase
from django.conf import settings
from pharmacy.models import Pharmacy

# Create your views here.
# def reg_deliveryagent(request):
#     pharmacy = request.session["uid"]
#     if request.method == "POST":
#         obj=Deliveryagent()
#         obj.name=request.POST.get('name')
#         obj.age=request.POST.get('age')
#         obj.address=request.POST.get('address')
#         obj.phno=request.POST.get('contact')
#         obj.email=request.POST.get('email')
#         obj.gender=request.POST.get('gender')
#         myfile = request.FILES["license"]
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name,myfile)
#         obj.license = myfile.name
#         obj.pha_id = pharmacy
#         obj.save()
#
#         ob = Login()
#         ob.username = request.POST.get('email')
#         ob.password = request.POST.get('contact')
#         ob.type = 'deliveryagent'
#         ob.u_id = obj.da_id
#         ob.save()
#
#         objlist = "Delivery agent Registered Successfully.."
#         context = {
#             'msg': objlist
#         }
#         return render(request, 'deliveryagent/reg_deliveryagent.html', context)
#     return render(request,'deliveryagent/reg_deliveryagent.html')

def reg_deliveryagent(request):
    pharmacy = request.session.get("uid")

    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        phno = request.POST.get('contact')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        license_file = request.FILES.get("license")

        # Validate fields
        if not all([name, age, address, phno, email, gender, license_file]):
            return render(request, 'deliveryagent/reg_deliveryagent.html', {
                'error': "All fields are required."
            })

        if not phno.isdigit() or len(phno) != 10:
            return render(request, 'deliveryagent/reg_deliveryagent.html', {
                'error': "Phone number must be exactly 10 digits."
            })

        try:
            age_int = int(age)
            if age_int <= 0:
                raise ValueError
        except ValueError:
            return render(request, 'deliveryagent/reg_deliveryagent.html', {
                'error': "Age must be a positive number."
            })

        if Deliveryagent.objects.filter(email=email).exists():
            return render(request, 'deliveryagent/reg_deliveryagent.html', {
                'error': "A delivery agent with this email already exists."
            })

        # Save license file
        fs = FileSystemStorage()
        filename = fs.save(license_file.name, license_file)

        # Save Delivery Agent
        agent = Deliveryagent(
            name=name,
            age=age_int,
            address=address,
            phno=phno,
            email=email,
            gender=gender,
            license=filename,
            pha_id=pharmacy
        )
        agent.save()

        # Save Login
        login = Login(
            username=email,
            password=phno,
            type='deliveryagent',
            u_id=agent.da_id
        )
        login.save()

        return render(request, 'deliveryagent/reg_deliveryagent.html', {
            'msg': "Delivery agent registered successfully."
        })

    return render(request, 'deliveryagent/reg_deliveryagent.html')

def viewdeliveryagent(request):
    da = request.session["uid"]
    obj = Deliveryagent.objects.filter(pha_id=da)
    context = {
        'ab': obj,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'deliveryagent/viewdeliveryagent.html',context)

def delete(request,idd):
    obj=Deliveryagent.objects.get(da_id=idd).delete()
    return viewdeliveryagent(request)


# def assign(request):
#     ord = request.session["uid"]
#     obj=Deliveryagent.objects.filter(pharmacy_id=ord)
#
#     context ={
#
#         'ac':obj,
#     }
#     if request.method == "POST":
#         da_id = request.POST.get("da_id")
#         pu_id = request.POST.get("pu_id")
#         ob=Delivery()
#         ob.status='pending'
#         ob.date=datetime.datetime.today()
#         ob.time=datetime.datetime.today()
#         ob.deliveryagent_id=da_id
#         ob.purchase_id=pu_id
#         ob.save()
#     return render(request,'deliveryagent/assign_delivery.html',context)

# def assign(request):
#     ord = request.session.get("uid")
#     delivery_agents = Deliveryagent.objects.filter(pha_id=ord)
#
#     pu_id = request.GET.get("pu_id")
#     da_id = request.GET.get("da_id")
#
#     purchases = Purchase.objects.filter(pu_id=pu_id) if pu_id else []
#
#     message = None
#
#     if da_id and pu_id:
#         # Check if already assigned
#         if not Delivery.objects.filter(purchase_id=pu_id).exists():
#             Delivery.objects.create(
#                 deliveryagent_id=da_id,
#                 purchase_id=pu_id,
#                 status="pending",
#                 date=datetime.date.today(),
#                 time=datetime.datetime.now().time()
#             )
#             message = "Delivery assigned successfully."
#         else:
#             message = "This purchase already has a delivery agent."
#
#     context = {
#         'ac': delivery_agents,
#         'purchases': purchases,
#         'message': message
#     }
#
#     return render(request, 'deliveryagent/assign_delivery.html', context)

def assign(request):
    ord = request.session.get("uid")  # pharmacy ID from session
    delivery_agents = Deliveryagent.objects.filter(pha_id=ord)

    pu_id = request.GET.get("pu_id")
    da_id = request.GET.get("da_id")

    purchases = Purchase.objects.filter(pu_id=pu_id) if pu_id else Purchase.objects.none()

    message = None

    if da_id and pu_id:
        # Check if already assigned
        if not Delivery.objects.filter(purchase_id=pu_id).exists():
            try:
                purchase_obj = Purchase.objects.get(pu_id=pu_id)

                Delivery.objects.create(
                    deliveryagent_id=da_id,
                    purchase_id=pu_id,
                    status="pending",
                    date=datetime.date.today(),
                    time=datetime.datetime.now().time(),
                    pha_id=purchase_obj.pharmacy,       # saving pharmacy from Purchase
                    p_id=purchase_obj.patient           # saving patient from Purchase
                )
                message = "Delivery assigned successfully."
            except Purchase.DoesNotExist:
                message = "Invalid purchase ID."

        else:
            message = "This purchase already has a delivery agent."

    context = {
        'ac': delivery_agents,
        'purchases': purchases,
        'message': message
    }

    return render(request, 'deliveryagent/assign_delivery.html', context)