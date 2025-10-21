from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import RazorpayPayment
import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def payment_form(request):
    if request.method == "POST":
        name = request.POST['name']
        amount = int(request.POST['amount']) * 100  # INR to paise

        order = client.order.create(dict(amount=amount, currency='INR', payment_capture='1'))

        payment = RazorpayPayment.objects.create(
            name=name,
            user=request.user if request.user.is_authenticated else None,
            amount=amount,
            order_id=order['id']
        )

        context = {
            'payment': payment,
            'order': order,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        }
        return render(request, 'payment/payment_checkout.html', context)

    return render(request, 'payment/payment_form.html')
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        payment = RazorpayPayment.objects.get(order_id=data['razorpay_order_id'])

        payment.payment_id = data['razorpay_payment_id']
        payment.signature = data['razorpay_signature']
        payment.paid = True
        payment.save()

        return render(request, 'payment/payment_success.html', {'payment': payment})

    return render(request, 'payment/payment_failed.html')
