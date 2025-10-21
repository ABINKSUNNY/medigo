from django.shortcuts import render
from doctor.models import *
from login.models import Login
from hospital.models import Hospital


# Create your views here.
def adminview_doc(request):
    obj=Doctor.objects.filter(status="pending")
    context = {
        'obj':obj
    }
    return render(request,'doctor/adminview_doc.html',context)

def approve(request,idd):
    obj=Doctor.objects.get(doc_id=idd)
    obj.status = "approved"
    obj.save()
    return adminview_doc(request)

def reject(request,idd):
    obj=Doctor.objects.get(doc_id=idd)
    obj.status = "rejected"
    obj.save()
    return adminview_doc(request)

def delete(request,idd):
    obj=Doctor.objects.get(doc_id=idd).delete()
    return hospitalview_doc(request)



def hospitalview_doc(request):
    hospital_id = request.session.get("uid")
    obj=Doctor.objects.filter(hospital_id=hospital_id)
    context = {
        'obj':obj
    }
    return render(request,'doctor/hospitalview_doc.html',context)

from django.shortcuts import render
from doctor.models import Doctor
from login.models import Login

# def reg_doc(request):
#     if request.method == "POST":
#         hospital_id = request.session.get("uid")  # Assuming this is set during hospital login
#
#         if not hospital_id:
#             return render(request, 'doctor/reg_doc.html', {'error': 'Hospital login required to register a doctor.'})
#
#         obj = Doctor()
#         obj.doc_name = request.POST.get('doc_name')
#         obj.email = request.POST.get('email')
#         obj.contact = request.POST.get('contact')
#         obj.gender = request.POST.get('gender')
#         obj.doc_age = request.POST.get('doc_age')
#         obj.consulting_hour = request.POST.get('cousulting_hour')
#         obj.qualification = request.POST.get('qualification')
#         obj.specialization = request.POST.get('specilization')
#         obj.department = request.POST.get('deparment')
#         obj.status = "pending"
#         obj.hospital_id = hospital_id  # ✅ Save the hospital ID
#         obj.save()
#
#         ob = Login()
#         ob.username = request.POST.get('doc_name')
#         ob.password = request.POST.get('contact')  # Default password = contact number
#         ob.type = 'doctor'
#         ob.u_id = obj.doc_id
#         ob.save()
#
#         context = {'msg': "Doctor Registered Successfully.."}
#         return render(request, 'doctor/reg_doc.html', context)
#
#     return render(request, 'doctor/reg_doc.html')
def reg_doc(request):
    if request.method == "POST":
        hospital_id = request.session.get("uid")

        if not hospital_id:
            return render(request, 'doctor/reg_doc.html', {
                'error': 'Hospital login required to register a doctor.'
            })

        # Extract form data
        doc_name = request.POST.get('doc_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        doc_age = request.POST.get('doc_age')
        consulting_hour = request.POST.get('cousulting_hour')
        qualification = request.POST.get('qualification')
        specialization = request.POST.get('specilization')
        department = request.POST.get('deparment')
        consultation_fee = request.POST.get('consultation_fee')

        # Check for empty fields
        if not all([doc_name, email, contact, gender, doc_age, consulting_hour, consultation_fee , qualification, specialization, department]):
            return render(request, 'doctor/reg_doc.html', {
                'error': "All fields are required."
            })

        # Phone number validation
        if not contact.isdigit() or len(contact) != 10:
            return render(request, 'doctor/reg_doc.html', {
                'error': "Contact number must be exactly 10 digits."
            })

        # Age validation
        try:
            age = int(doc_age)
            if age <= 0:
                raise ValueError
        except ValueError:
            return render(request, 'doctor/reg_doc.html', {
                'error': "Age must be a positive number."
            })

        # Email uniqueness check
        if Doctor.objects.filter(email=email).exists():
            return render(request, 'doctor/reg_doc.html', {
                'error': "A doctor with this email already exists."
            })

        # Save doctor
        doc = Doctor(
            doc_name=doc_name,
            email=email,
            contact=contact,
            gender=gender,
            doc_age=age,
            consulting_hour=consulting_hour,
            qualification=qualification,
            specialization=specialization,
            department=department,
            status="pending",
            hospital_id=hospital_id,
            consultation_fee=consultation_fee,
        )
        doc.save()

        # Save login info
        login = Login(
            username=email,
            password=contact,  # Using contact number as default password
            type='doctor',
            u_id=doc.doc_id
        )
        login.save()

        return render(request, 'doctor/reg_doc.html', {
            'msg': "Doctor registered successfully."
        })

    return render(request, 'doctor/reg_doc.html')