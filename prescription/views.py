from datetime import datetime
from patient.models import Patient
from django.shortcuts import render,redirect
from prescription.models import *
from django.http import FileResponse, Http404
from .models import Prescription
import os
from django.conf import settings






# def download_prescription(request, pres_id):
#     try:
#         prescription = Prescription.objects.get(pres_id=pres_id)
#
#         # Get the file path depending on field type
#         file_field = prescription.prescription
#         file_name = file_field.name if hasattr(file_field, 'name') else file_field
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#
#         if not file_field:
#             raise Http404("No file uploaded for this prescription.")
#
#         if os.path.exists(file_path):
#             return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
#         else:
#             raise Http404("Prescription file not found.")
#
#     except Prescription.DoesNotExist:
#         raise Http404("Prescription not found.")
def download_prescription(request, pres_id):
    try:
        prescription = Prescription.objects.get(pres_id=pres_id)
        file_name = prescription.prescription.strip()

        if not file_name:
            raise Http404("No file uploaded for this prescription.")

        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
        else:
            raise Http404("Prescription file not found.")
    except Prescription.DoesNotExist:
        raise Http404("Prescription not found.")


# Create your views here.
# def add_pres(request):
#     aa=request.session["uid"]
#     if request.method == 'POST':
#         obj=Prescription()
#         obj.patient_id=request.POST.get('name')
#         obj.patient_id=request.POST.get('contact')
#         obj.doc_id=aa
#         obj.prescription=request.POST.get('prescription')
#         obj.date=datetime.today()
#         obj.time=datetime.today()
#         obj.save()
#
#     return render(request, 'prescription/add_pres.html')


# def add_pres(request):
#     aa =  request.session["uid"]
#
#     if request.method == 'POST':
#         name = request.POST.get('name').strip()
#         contact = request.POST.get('contact').strip()
#         uploaded_file = request.FILES.get('prescription')  # ✅ Get uploaded file
#
#         try:
#             # Match both name and contact number
#             patient = Patient.objects.get(name=name, phno=contact)
#         except Patient.DoesNotExist:
#             return render(request, 'prescription/add_pres.html', {
#                 'error': 'No patient found with the given name and contact.'
#             })
#
#         Prescription.objects.create(
#             patient=patient,
#             doctor_id=aa,
#             prescription=uploaded_file,  # ✅ Save the file
#             date=datetime.today().date(),
#             time=datetime.today().time()
#         )
#
#         return render(request, 'prescription/add_pres.html', {
#             'success': 'Prescription uploaded successfully.'
#         })
#
#     return render(request, 'prescription/add_pres.html')

def add_pres(request):
    aa = request.session["uid"]

    if request.method == 'POST':
        name = request.POST.get('name').strip()
        contact = request.POST.get('contact').strip()
        uploaded_file = request.FILES.get('prescription')  # Uploaded image file

        try:
            patient = Patient.objects.get(name=name, phno=contact)
        except Patient.DoesNotExist:
            return render(request, 'prescription/add_pres.html', {
                'error': 'No patient found with the given name and contact.'
            })

        # Save the uploaded file to MEDIA_ROOT/prescriptions/
        file_name = f"prescriptions/{uploaded_file.name}"
        save_path = os.path.join(settings.MEDIA_ROOT, file_name)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        Prescription.objects.create(
            patient=patient,
            doctor_id=aa,
            prescription=file_name,  # Just the relative path saved
            date=datetime.today().date(),
            time=datetime.today().time()
        )

        return render(request, 'prescription/add_pres.html', {
            'success': 'Prescription uploaded successfully.'
        })

    return render(request, 'prescription/add_pres.html')


# def view_pres(request):
#     aa = request.session["uid"]
#     obj=Prescription.objects.filter(patient_id=aa)
#     context = {
#         'obj':obj
#     }
#     return render(request,'prescription/view_pres.html',context)
def view_pres(request):
    aa = request.session["uid"]
    obj = Prescription.objects.filter(patient_id=aa)
    return render(request, 'prescription/view_pres.html', {'obj': obj})