# app/context_processors.py
from appointment.models import Appointment
from chat.models import Chat

def unseen_notifications(request):
    patient_id = request.session.get("uid")
    if patient_id:
        unseen_count = Appointment.objects.filter(patient_id=patient_id, is_seen=False).count()
        unseen_appointments = Appointment.objects.filter(patient_id=patient_id, is_seen=False).order_by('-date', '-time')[:5]
    else:
        unseen_count = 0
        unseen_appointments = []

    return {
        'unseen_notifications_count': unseen_count,
        'unseen_appointments': unseen_appointments,
    }


# app/context_processors.py


def unseen_chat_notifications(request):
    patient_id = request.session.get("uid")
    unseen_chats_count = 0
    if patient_id:
        unseen_chats_count = Chat.objects.filter(
            p_id=patient_id,
            to_type='patient',
            from_type='doctor',
            seen=0
        ).count()
    return {'unseen_chats_count': unseen_chats_count}
