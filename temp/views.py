# from django.shortcuts import render
# from appointment.models import Appointment
#
# # Create your views here.
# def index(request):
#     return render(request,'temp/index.html')
#
# def admin_home(request):
#     return render(request,'temp/admin_home.html')
#
# def deliveryagent_home(request):
#     return render(request,'temp/deliveryagent_home.html')
#
# def doc_home(request):
#     return render(request,'temp/doc_home.html')
#
# def hospital_home(request):
#     return render(request,'temp/hospital_home.html')
#
# # def patient_home(request):
# #     return render(request,'temp/patient_home.html')
#
# def patient_home(request):
#     uid = request.session.get("uid")
#     unseen_notifications_count = 0
#     if uid:
#         unseen_notifications_count = Appointment.objects.filter(patient_id=uid, is_seen=False).count()
#
#     context = {
#         'unseen_notifications_count': unseen_notifications_count,
#     }
#     return render(request, 'patient_home.html', context)
#
# def pharmacy_home(request):
#     return render(request,'temp/pharmacy_home.html')
#


from django.shortcuts import render
# from appointment.models import Appointment
#
# # Helper function
# def get_unseen_notification_count(request):
#     uid = request.session.get("uid")
#     if uid:
#         return Appointment.objects.filter(patient_id=uid, is_seen=False).count()
#     return 0

def index(request):
    return render(request, 'temp/index.html', )

def admin_home(request):

    return render(request, 'temp/admin_home.html')

def deliveryagent_home(request):

    return render(request, 'temp/deliveryagent_home.html')

def doc_home(request):

    return render(request, 'temp/doc_home.html',)

def hospital_home(request):

    return render(request, 'temp/hospital_home.html', )

def patient_home(request):

    return render(request, 'temp/patient_home.html', )

def pharmacy_home(request):

    return render(request, 'temp/pharmacy_home.html',)
