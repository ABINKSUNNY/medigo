from django.shortcuts import render,redirect,get_object_or_404
from appointment.models import Appointment
from hospital.models import Hospital
from doctor.models import Doctor
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from chat.models import Chat
from django.utils import timezone
from datetime import datetime,timedelta
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.mail import send_mail



from django.db.models import Q

# View to manage pending appointments
def manageappointment(request):
    hos=request.session["uid"]
    obj = Appointment.objects.filter(status="pending",hospital_id=hos)
    context = {
        'ab': obj
    }
    return render(request, 'appointment/manageappointment.html', context)

# View to display all appointments
def view_app(request):
    hospital_id= request.session.get("uid")
    date = request.GET.get('date')
    if date:
        try:
            objdate = datetime.strptime(date, "%Y-%m-%d").date()
            obj = Appointment.objects.filter(hospital_id=hospital_id, date=objdate)
        except ValueError:
            obj = Appointment.objects.filter(hospital_id=hospital_id)
            # obj = []
    else:
        obj = Appointment.objects.filter(hospital_id=hospital_id)
        # obj = []


    context = {
        'cd': obj,
        'selected_date': date or ''
    }
    return render(request, 'appointment/viewappointment.html', context)






# def user_app(request):
#     doctors = Doctor.objects.select_related("hospital").all()
#     msg = ""
#
#     # -- SEARCH LOGIC --
#     query = request.GET.get("search", "").strip()
#     filter_by = request.GET.get("filter_by")
#     if query and filter_by in ("department", "hospital", "doctor", "address"):
#         lookup_map = {
#             "department": ["department__icontains", "hospital__department__icontains"],
#             "hospital": ["hospital__hospitalname__icontains"],
#             "doctor": ["doc_name__icontains"],
#             "address": ["hospital__address__icontains"],
#         }
#         qobj = Q()
#         for lk in lookup_map[filter_by]:
#             qobj |= Q(**{lk: query})
#         doctors = doctors.filter(qobj)
#
#     # -- BOOKING LOGIC with validations --
#     if request.method == "POST":
#         hospital_id = request.POST.get("hospital_id")
#         doctor_id = request.POST.get("doctor_id")
#         date_str = request.POST.get("date")    # "YYYY-MM-DD"
#         time_str = request.POST.get("time")    # "HH:MM"
#         appt_type = request.POST.get("type")
#         patient_id = request.session.get("uid")
#
#         # Parse date + time into timezone-aware datetime
#         try:
#             naive = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
#             requested_dt = timezone.make_aware(naive, timezone.get_current_timezone())
#         except ValueError:
#             msg = "Invalid date/time format."
#             return render(request, "appointment/userappointment.html", {"ob": doctors, "msg": msg})
#
#         now = timezone.now()
#         if requested_dt < now:
#             msg = "Cannot book an appointment in the past."
#         else:
#             buffer = datetime.timedelta(minutes=2)
#             start_win = (requested_dt - buffer).time()
#             end_win = (requested_dt + buffer).time()
#
#             # 🛠️ Correct conflict check: direct date lookup, no __date usage
#             conflicts = Appointment.objects.filter(
#                 doctor_id=doctor_id,
#                 date=requested_dt.date(),
#                 time__range=(start_win, end_win)
#             )
#             if conflicts.exists():
#                 msg = "This slot is unavailable (within ±2 minutes of another booking)."
#             else:
#                 Appointment.objects.create(
#                     patient_id=patient_id,
#                     hospital_id=hospital_id,
#                     doctor_id=doctor_id,
#                     date=date_str,
#                     time=time_str,
#                     type=appt_type,
#                     status="pending",
#                 )
#                 msg = (
#                     "Appointment booked successfully!\n\n"
#                     "❗ For ONLINE consultations, please check your appointment status regularly. "
#                     "Once approved, complete the payment."
#                 )
#
#     return render(request, "appointment/userappointment.html", {"ob": doctors, "msg": msg})
# ***************************************************************

def user_app(request):
    doctors = Doctor.objects.select_related("hospital").all()
    msg = ""

    # -- SEARCH LOGIC --
    query = request.GET.get("search", "").strip()
    filter_by = request.GET.get("filter_by")
    if query and filter_by in ("department", "hospital", "doctor", "address"):
        lookup_map = {
            "department": ["department__icontains", "hospital__department__icontains"],
            "hospital": ["hospital__hospitalname__icontains"],
            "doctor": ["doc_name__icontains"],
            "address": ["hospital__address__icontains"],
        }
        qobj = Q()
        for lk in lookup_map[filter_by]:
            qobj |= Q(**{lk: query})
        doctors = doctors.filter(qobj)

    # -- BOOKING LOGIC with validations --
    if request.method == "POST":
        hospital_id = request.POST.get("hospital_id")
        doctor_id = request.POST.get("doctor_id")
        date_str = request.POST.get("date")    # "YYYY-MM-DD"
        time_str = request.POST.get("time")    # "HH:MM"
        appt_type = request.POST.get("type")
        patient_id = request.session.get("uid")

        # Use direct datetime import
        try:
            naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            requested_dt = timezone.make_aware(naive, timezone.get_current_timezone())
        except ValueError:
            msg = "Invalid date/time format."
            return render(request, "appointment/userappointment.html", {"ob": doctors, "msg": msg})

        now = timezone.now()
        if requested_dt < now:
            msg = "Cannot book an appointment in the past."
        else:
            buffer = timedelta(minutes=2)
            start_win = (requested_dt - buffer).time()
            end_win = (requested_dt + buffer).time()

            conflicts = Appointment.objects.filter(
                doctor_id=doctor_id,
                date=requested_dt.date(),
                time__range=(start_win, end_win)
            )
            if conflicts.exists():
                msg = "This slot is unavailable (within ±2 minutes of another booking)."
            else:
                Appointment.objects.create(
                    patient_id=patient_id,
                    hospital_id=hospital_id,
                    doctor_id=doctor_id,
                    date=date_str,
                    time=time_str,
                    type=appt_type,
                    status="pending",
                )
                msg = (
                    "Appointment booked successfully!\n\n"
                    "❗ For ONLINE consultations, please check your appointment status regularly. "
                    "Once approved, complete the payment."
                )

    return render(request, "appointment/userappointment.html", {"ob": doctors, "msg": msg})
# ***********************************************************


# Approve an appointment
def approve_app(request, idd):
    obj = Appointment.objects.get(a_id=idd)
    obj.status = "Payment Pending"
    obj.is_seen = False
    obj.save()
    return redirect('manageappointment')

# Reject an appointment
def reject_app(request, idd):
    obj = Appointment.objects.get(a_id=idd)
    obj.status = "rejected"
    obj.is_seen = False
    obj.save()
    return redirect('manageappointment')



def patientview_app(request):
    patient_id = request.session.get("uid")
    obj = Appointment.objects.filter(patient_id=patient_id)

    unseen_count = Appointment.objects.filter(patient_id=patient_id, is_seen=False).count()
    unseen_appointments = Appointment.objects.filter(patient_id=patient_id, is_seen=False).order_by('-date', '-time')[:5]

    # Mark as seen now that patient opened the page
    Appointment.objects.filter(patient_id=patient_id, is_seen=False).update(is_seen=True)

    context = {
        'cb': obj,
        'unseen_notifications_count': unseen_count,
        'unseen_appointments': unseen_appointments,
    }
    return render(request, 'appointment/patientview_app.html', context)





def docview_app(request):
    doctor_id = request.session.get("uid")
    date_query = request.GET.get('date')  # Get the selected date from the form

    if date_query:
        try:
            date_obj = datetime.strptime(date_query, "%Y-%m-%d").date()
            obj = Appointment.objects.filter(doctor_id=doctor_id, date=date_obj)
        except ValueError:
            obj = Appointment.objects.filter(doctor_id=doctor_id)
    else:
        obj = Appointment.objects.filter(doctor_id=doctor_id)

    context = {
        'cd': obj,
        'selected_date': date_query or ''
    }

    return render(request, 'appointment/doc_view.html', context)

def chat(request, idd):
    appointment = Appointment.objects.get(a_id=idd)
    context = {
        'cd': [appointment]
    }

    doctor_id = request.session["uid"]

    if request.method == 'POST':
        msg = request.POST.get('msg')

        Chat.objects.create(
            chat=msg,
            doctor_id=doctor_id,
            p_id=appointment.patient,  # assign Patient instance, not ID
            date=datetime.today().date(),
            time=datetime.now().time(),
            from_type="doctor",
            to_type="patient",
            seen=0
        )

        return redirect('chat', idd=idd)

    return render(request, 'chat/chat.html', context)



from django.urls import reverse



def pay_now(request, a_id):
    appointment = get_object_or_404(Appointment, a_id=a_id)
    fee = appointment.doctor.consultation_fee or 0  # default ₹0 if missing

    if request.method == "POST":
        amount = fee  # ignore user input
        request.session['pay_amount'] = amount * 100
        request.session['appointment_id'] = a_id
        return redirect(reverse('initiate_payment') + '#payment-section')

    return render(request, 'appointment/enter_amount.html', {
        'appointment': appointment,
        'fee': fee
    })



def initiate_payment(request):
    amount = request.session.get('pay_amount')
    a_id = request.session.get('appointment_id')

    if not amount or not a_id:
        return HttpResponse("Missing payment data", status=400)

    appointment = get_object_or_404(Appointment, a_id=a_id)
    appointment.amount = amount // 100  # store ₹ amount
    appointment.save()

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "appointment": appointment,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }
    return render(request, "appointment/razorpay_payment.html", context)


# @csrf_exempt
# def payment_success(request):
#     if request.method == "POST":
#         razorpay_payment_id = request.POST.get("razorpay_payment_id")
#         a_id = request.POST.get("appointment_id")
#         if not razorpay_payment_id or not a_id:
#             return HttpResponse("Missing data", status=400)
#
#         appointment = get_object_or_404(Appointment, a_id=a_id)
#         appointment.payment_id = razorpay_payment_id
#         appointment.status = "paid"
#
#         now = datetime.now()
#         appointment.payment_date = now.date()
#         appointment.payment_time = now.time()
#         appointment.save()
#
#         return redirect('patientapp')
#
#     return HttpResponse("Invalid request", status=400)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        a_id = request.POST.get("appointment_id")
        if not razorpay_payment_id or not a_id:
            return HttpResponse("Missing data", status=400)

        appointment = get_object_or_404(Appointment, a_id=a_id)
        appointment.payment_id = razorpay_payment_id
        appointment.status = "paid"

        now = datetime.now()
        appointment.payment_date = now.date()
        appointment.payment_time = now.time()
        appointment.save()

        # ✅ Send email on payment
        try:
            send_mail(
                subject="Appointment Payment Successful",
                message=f"Dear {appointment.patient.name},\n\nYour payment for appointment #{appointment.a_id} has been successfully received.\n\nAppointment Details:\nDate: {appointment.date}\nTime: {appointment.time}\nDoctor: {appointment.doctor.doc_name}\nHospital: {appointment.hospital.hospitalname}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[appointment.patient.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Payment email failed to send: {e}")

        return redirect('patientapp')

    return HttpResponse("Invalid request", status=400)


def hpayment(request):
    hospital = request.session.get("uid")
    obj = Appointment.objects.filter(hospital_id=hospital)
    context ={
        'cd':obj,
    }
    return render(request,"appointment/hpayment.html",context)



# @require_POST
# def cancel_appointment(request, a_id):
#     appt = get_object_or_404(Appointment, a_id=a_id, patient_id=request.session.get('uid'))
#     appt.status = "cancelled"
#     appt.save()
#     messages.success(request, f"Appointment #{a_id} canceled.")
#     return redirect(reverse('patientapp') + '#c')

@require_POST
def cancel_appointment(request, a_id):
    appt = get_object_or_404(Appointment, a_id=a_id, patient_id=request.session.get('uid'))
    appt.status = "cancelled"
    appt.save()

    # ✅ Send email on cancellation
    try:
        send_mail(
            subject="Appointment Cancelled",
            message=f"Dear {appt.patient.name},\n\nYour appointment #{a_id} has been cancelled successfully.\n\nDate: {appt.date}\nTime: {appt.time}\nDoctor: {appt.doctor.doc_name}\nHospital: {appt.hospital.hospitalname}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appt.patient.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Cancellation email failed to send: {e}")

    messages.success(request, f"Appointment #{a_id} canceled.")
    return redirect(reverse('patientapp') + '#c')


# @require_POST
# def cancel_appointmenthos(request, a_id):
#     appt = get_object_or_404(Appointment, a_id=a_id, hospital_id=request.session.get('uid'))
#     appt.status = "cancelled"
#     appt.save()
#     messages.success(request, f"Appointment #{a_id} canceled.")
#     return redirect('viewapp')


@require_POST
def cancel_appointmenthos(request, a_id):
    appt = get_object_or_404(Appointment, a_id=a_id, hospital_id=request.session.get('uid'))
    appt.status = "cancelled"
    appt.save()

    # ✅ Send email on hospital cancellation
    try:
        send_mail(
            subject="Appointment Cancelled by Hospital",
            message=f"Dear {appt.patient.name},\n\nWe regret to inform you that your appointment #{a_id} has been cancelled by the hospital.\n\nDate: {appt.date}\nTime: {appt.time}\nDoctor: {appt.doctor.doc_name}\nHospital: {appt.hospital.hospitalname}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appt.patient.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Hospital cancellation email failed to send: {e}")

    messages.success(request, f"Appointment #{a_id} canceled.")
    return redirect('viewapp')
