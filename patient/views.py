from django.shortcuts import render
from patient.models import Patient
from login.models import Login

# Create your views here.
def adminmanage_patient(request):
    obj = Patient.objects.all()
    context = {
        'ob':obj
    }
    return render(request,'patient/adminmanage_patient.html',context)

# def reg_patient(request):
#     if request.method == "POST":
#         obj=Patient()
#         obj.name=request.POST.get('name')
#         obj.age=request.POST.get('age')
#         obj.gender=request.POST.get('gender')
#         obj.phno=request.POST.get('contact')
#         obj.address=request.POST.get('address')
#         obj.email=request.POST.get('email')
#         obj.password=request.POST.get('password')
#         obj.repass=request.POST.get('repass')
#         obj.save()
#
#         ob=Login()
#         ob.username=request.POST.get('email')
#         ob.password=request.POST.get('password')
#         ob.type='patient'
#         ob.u_id=obj.p_id
#         ob.save()
#
#         objlist ="patient Registered Successfully.."
#         context ={
#             'msg':objlist
#         }
#         return  render(request,'patient/reg_patient.html',context)
#
#     return render(request,'patient/reg_patient.html')
def reg_patient(request):
    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repass = request.POST.get('repass')

        # Validation
        if not all([name, age, gender, contact, address, email, password, repass]):
            return render(request, 'patient/reg_patient.html', {'error': 'All fields are required.'})

        if not contact.isdigit() or len(contact) != 10:
            return render(request, 'patient/reg_patient.html', {'error': 'Phone number must be exactly 10 digits.'})

        # 🚫 Password minimum length validation
        if len(password) < 6:
            return render(request, 'patient/reg_patient.html', {'error': 'Password must be at least 6 characters long.'})

        if password != repass:
            return render(request, 'patient/reg_patient.html', {'error': 'Passwords do not match.'})

        if Login.objects.filter(username=email).exists():
            return render(request, 'patient/reg_patient.html', {'error': 'Email already registered.'})

        # Save Patient
        patient = Patient(
            name=name,
            age=age,
            gender=gender,
            phno=contact,
            address=address,
            email=email,
            password=password,
            repass=repass
        )
        patient.save()

        # Save Login (password stored as plain text; consider hashing in production)
        login = Login(
            username=email,
            password=password,
            type='patient',
            u_id=patient.p_id
        )
        login.save()

        return render(request, 'patient/reg_patient.html', {'msg': 'Patient Registered Successfully.'})

    return render(request, 'patient/reg_patient.html')

def delete(request, idd):
    obj=Patient.objects.get(p_id=idd).delete()
    return adminmanage_patient(request)

def patientview(request):
    obj = Patient.objects.all()
    context = {
        'ob':obj
    }
    return render(request,'patient/patientview.html',context)

def editview(request):
    aa=request.session["uid"]
    obj = Patient.objects.filter(p_id=aa)
    context = {
        'ob': obj
    }
    return render(request,'patient/profile_view.html',context)

def patient_edit(request, idd):
    obj = Patient.objects.filter(p_id=idd)
    aa = request.session["uid"]
    context = {
        'obj': obj,
    }

    if request.method == "POST":
        patient = Patient.objects.get(p_id=aa)
        patient.name = request.POST.get('name')
        patient.age = request.POST.get('age')
        patient.gender = request.POST.get('gender')
        patient.phno = request.POST.get('contact')
        patient.address = request.POST.get('address')
        patient.email = request.POST.get('email')
        patient.password = request.POST.get('password')
        patient.repass = request.POST.get('repass')
        patient.save()

        # Set message only after saving
        context['msg'] = "Profile Updated Successfully.."

    return render(request, 'patient/edit_patient.html', context)
