
import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from login.models import Login
from patient.models import Patient  # Import the Patient model


def login(request):
    if request.method == "POST":
        un = request.POST.get("username")
        ps = request.POST.get("password")

        if Login.objects.filter(username=un, password=ps).exists():
            login_obj = Login.objects.get(username=un, password=ps)
            uid = login_obj.u_id
            user_type = login_obj.type

            # Store UID in session
            request.session["uid"]  = uid

            if user_type == "admin":
                return render(request, 'temp/admin_home.html')
            elif user_type == "patient":
                # Optional: check if the Patient exists
                if Patient.objects.filter(p_id=uid).exists():
                    return render(request, 'temp/patient_home.html')
                else:
                    return render(request, 'login/login.html', {'inv': "Patient record not found."})

            elif user_type == "hospital":
                return render(request, 'temp/hospital_home.html')

            elif user_type == "pharmacy":
                return render(request, 'temp/pharmacy_home.html')

            elif user_type == "deliveryagent":
                return render(request, 'temp/deliveryagent_home.html')

            elif user_type == "doctor":
                return render(request, 'temp/doc_home.html')

            else:
                return render(request, 'login/login.html', {'inv': "Invalid user type."})
        else:
            return render(request, 'login/login.html', {'inv': "Incorrect username or password!!!"})

    return render(request, 'login/login.html')



#
# # Step 1: Forgot Password Request View
# def forgot_password_request(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         try:
#             user = Login.objects.get(username=username)
#             otp = str(random.randint(100000, 999999))
#             user.otp = otp
#             user.save()
#
#             # Send OTP via email
#             send_mail(
#                 'Your OTP for Password Reset',
#                 f'Your OTP is: {otp}',
#                 'medigo2025@gmail.com',       # From email (must match EMAIL_HOST_USER)
#                 [username],                   # To email (assuming username is email)
#                 fail_silently=False,
#             )
#
#             request.session['otp_user'] = username
#             return redirect('verify_otp')
#
#         except Login.DoesNotExist:
#             return render(request, 'login/forgot_password_request.html', {'error': "Username not found."})
#
#     return render(request, 'login/forgot_password_request.html')
#
#
# # Step 2: Verify OTP View
# def verify_otp(request):
#     if request.method == "POST":
#         otp_entered = request.POST.get("otp")
#         new_password = request.POST.get("new_password")
#         username = request.session.get('otp_user')
#
#         if username:
#             try:
#                 user = Login.objects.get(username=username)
#                 if user.otp == otp_entered:
#                     user.password = new_password
#                     user.otp = None  # Clear OTP
#                     user.save()
#                     del request.session['otp_user']
#                     return redirect('login')
#                 else:
#                     return render(request, 'login/verify_otp.html', {'error': "Invalid OTP."})
#             except Login.DoesNotExist:
#                 return redirect('forgot_password_request')
#
#     return render(request, 'login/verify_otp.html')



def forgot_password_request(request):
    if request.method == "POST":
        username = request.POST.get("username")

        try:
            user = Login.objects.get(username=username)
            otp = str(random.randint(100000, 999999))

            # Store OTP and username in session
            request.session['otp'] = otp
            request.session['otp_user'] = username

            # Send OTP via email
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is: {otp}',
                'medigo2025@gmail.com',
                [username],  # assuming username is an email
                fail_silently=False,
            )

            return redirect('verify_otp')

        except Login.DoesNotExist:
            return render(request, 'login/forgot_password_request.html', {'error': "Username not found."})

    return render(request, 'login/forgot_password_request.html')


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        saved_otp = request.session.get("otp")
        username = request.session.get("otp_user")

        if entered_otp == saved_otp:
            try:
                user = Login.objects.get(username=username)
                user.password = new_password
                user.save(update_fields=['password'])

                # Clear session
                request.session.pop("otp", None)
                request.session.pop("otp_user", None)

                return redirect('login')
            except Login.DoesNotExist:
                return redirect('forgot_password_request')
        else:
            return render(request, 'login/verify_otp.html', {'error': "Invalid OTP."})

    return render(request, 'login/verify_otp.html')