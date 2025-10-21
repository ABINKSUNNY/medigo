from django.shortcuts import render,redirect,get_object_or_404
from chat.models import Chat
from appointment.models import Appointment
from patient.models import Patient
from doctor.models import Doctor
import datetime
# Create your views here.
# def chat(request):
#     cc=request.session["uid"]
#     vv=request.session["uid"]
#     if request.method =='POST':
#         obj=Chat()
#         obj.chat=request.POST.get('msg')
#         obj.doc_id=vv
#         obj.p_id=cc
#         obj.date=datetime.datetime.today()
#         obj.time=datetime.datetime.today()
#         obj.from_type="doctor"
#         obj.to_type="patient"
#         obj.save()
#     return render(request,'chat/chat.html')


# def chat(request):
#     doc_id = request.session.get("uid")  # assuming doctor is logged in
#
#     if request.method == 'POST':
#         patient_id = request.POST.get('p_id')  # should be passed in the form
#         message = request.POST.get('msg')
#
#         if patient_id and message:
#             Chat.objects.create(
#                 chat=message,
#                 doctor_id=doc_id,
#                 patient_id=patient_id,
#                 date=datetime.date.today(),
#                 time=datetime.datetime.now().time(),
#                 from_type="doctor",
#                 to_type="patient",
#                 seen=0  # unseen when sent
#             )
#             return redirect('chat')  # or to the chat room page
#
#     return render(request, 'chat/chat.html')

def chat(request, idd):
    doc_id = request.session.get("uid")  # Doctor ID from session
    doctor = get_object_or_404(Doctor, doc_id=doc_id)
    appointment = get_object_or_404(Appointment, a_id=idd)
    patient = appointment.patient  # ✅ Already a Patient instance

    if request.method == 'POST':
        message = request.POST.get('msg')
        if message:
            Chat.objects.create(
                chat=message,
                doctor=doctor,    # ✅ Doctor instance
                p_id=patient,     # ✅ Patient instance
                date=datetime.date.today(),
                time=datetime.datetime.now().time(),
                from_type="doctor",
                to_type="patient",
                seen=0
            )
            return redirect('chat', idd=idd)

    return render(request, 'chat/chat.html', {
        'patient': patient,
        'appointment': appointment
    })
# def viewchat(request):
#     pat=request.session["uid"]
#     ob=Chat.objects.filter(p_id=pat)
#     context={
#         'ob':ob
#
#     }
#     return render(request,'chat/viewchat.html',context)
#


#
# def viewchat(request):
#     pat = request.session["uid"]
#
#     # Mark messages from doctor to patient as seen
#     Chat.objects.filter(
#         p_id=pat,
#         to_type='patient',
#         from_type='doctor',
#         seen=0
#     ).update(seen=1)
#
#     # Redirect to re-run context processors with updated data
#     return redirect('viewchat')  # make sure 'viewchat' is your URL name


def viewchat(request):
    pat = request.session.get("uid")

    # Mark messages from doctor to patient as seen
    Chat.objects.filter(
        p_id=pat,
        to_type='patient',
        from_type='doctor',
        seen=0
    ).update(seen=1)

    # Fetch all chat messages
    chats = Chat.objects.filter(p_id=pat)

    context = {
        'ob': chats
    }
    return render(request, 'chat/viewchat.html', context)  # ✅ No redirect
