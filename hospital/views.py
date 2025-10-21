from django.shortcuts import render
from hospital.models import *
from login.models import Login
# Create your views here.

def manage_hos(request):
    obj=Hospital.objects.filter(status="pending")
    context = {
        'ab':obj
    }
    return render(request, 'hospital/manage_hos.html', context)


# def hos_reg(request):
# #     if request.method == 'POST':
# #        obj=Hospital()
# #        obj.hospitalname=request.POST.get('hospitalname')
# #        obj.email=request.POST.get('email')
# #        obj.department=','.join(request.POST.getlist('departments'))
# #        obj.speciality=request.POST.get('speciality')
# #        obj.contact=request.POST.get('contact')
# #        obj.address=request.POST.get('address')
# #        obj.status='pending'
# #        obj.password=request.POST.get('password')
# #        obj.repass=request.POST.get('repass')
# #        obj.save()
# #        objlist = "Hospital Registered Successfully.."
# #        context = {
# #            'msg': objlist
# #        }
# #        return render(request, 'hospital/hos_reg.html', context)
# #
# #
# #
# #     return render(request,'hospital/hos_reg.html')

def hos_reg(request):
    if request.method == 'POST':
        hospitalname = request.POST.get('hospitalname')
        email = request.POST.get('email')
        # departments = request.POST.getlist('departments')
        speciality = request.POST.get('speciality')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        password = request.POST.get('password')
        repass = request.POST.get('repass')

        # Check required fields
        if not all([hospitalname, email, speciality, contact, address, password, repass]):
            return render(request, 'hospital/hos_reg.html', {'error': 'All fields are required.'})

        # Contact number validation
        if not contact.isdigit() or len(contact) != 10:
            return render(request, 'hospital/hos_reg.html', {'error': 'Contact number must be exactly 10 digits.'})

        # 🚫 Password minimum length validation
        if len(password) < 6:
            return render(request, 'hospital/hos_reg.html', {'error': 'Password must be at least 6 characters long.'})

        # Password match validation
        if password != repass:
            return render(request, 'hospital/hos_reg.html', {'error': 'Passwords do not match.'})

        # Optional: Check if email already exists
        if Hospital.objects.filter(email=email).exists():
            return render(request, 'hospital/hos_reg.html', {'error': 'Email already registered.'})

        # Save the hospital
        obj = Hospital(
            hospitalname=hospitalname,
            email=email,
            # department=','.join(departments),
            speciality=speciality,
            contact=contact,
            address=address,
            password=password,
            repass=repass,
            status='pending'
        )
        obj.save()

        return render(request, 'hospital/hos_reg.html', {'msg': 'Hospital Registered Successfully.'})

    return render(request, 'hospital/hos_reg.html')

def userview_hos(request):
    obj=Hospital.objects.all()
    context={
        'ob':obj
    }
    return render(request,'hospital/userview_hos.html',context)

def approve_hos(request,idd):
    obj=Hospital.objects.get(h_id=idd)
    obj.status="approved"
    obj.save()
    ob = Login()
    ob.username = obj.email
    ob.password = obj.password
    ob.type = 'hospital'
    ob.u_id = obj.h_id
    ob.save()
    return manage_hos(request)



def reject_hos(request,idd):
    obj=Hospital.objects.get(h_id=idd)
    obj.status="rejected"
    obj.save()
    return manage_hos(request)

def admin_viewhos(request):
    obj=Hospital.objects.all()
    context={
        'ob':obj
    }
    return render(request,'hospital/admin_viewhos.html',context)

def delete(request,idd):
    obj=Hospital.objects.get(h_id=idd).delete()
    return admin_viewhos(request)