import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Product, CartItem, Purchase,Pharmacy
from patient.models import Patient

import os
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
# from .views import get_patient_and_session, get_cart_context

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



def get_patient_and_session(request):
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    patient_id = request.session.get("uid")
    patient = Patient.objects.filter(p_id=patient_id).first() if patient_id else None
    return patient, session_key

def view_products(request,idd):
    # cc=request.session["uid"]
    products = Product.objects.filter(pharmacy_id=idd)
    return render(request, 'cart/view_products.html', {'products': products})

def add_to_cart(request, product_id):
    patient, session_key = get_patient_and_session(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        patient=patient, session_key=session_key, product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Redirect using the correct custom primary key
    return redirect('view_products', idd=product.pharmacy.pha_id)


def cart(request):
    patient, session_key = get_patient_and_session(request)
    cart_items = CartItem.objects.filter(patient=patient, session_key=session_key)
    total = sum(item.get_total_price() for item in cart_items)

    razorpay_order = None
    if total > 0:
        razorpay_order = razorpay_client.order.create({
            'amount': int(total * 100),
            'currency': 'INR',
            'payment_capture': '1'
        })
        request.session['razorpay_order_id'] = razorpay_order['id']

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'razorpay_order_id': razorpay_order['id'] if razorpay_order else None,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': total
    })

def update_cart(request):
    if request.method == 'POST':
        patient, session_key = get_patient_and_session(request)
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        product = get_object_or_404(Product, id=product_id)

        cart_item = CartItem.objects.filter(
            patient=patient, session_key=session_key, product=product
        ).first()

        if cart_item:
            if action == 'add':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    return redirect('cart')

#
# @csrf_exempt
# def complete_payment(request):
#     if request.method == 'POST':
#         payment_id = request.POST.get('razorpay_payment_id')
#         order_id = request.session.get('razorpay_order_id')
#         patient, session_key = get_patient_and_session(request)
#         cart_items = CartItem.objects.filter(patient=patient, session_key=session_key)
#         total = sum(item.get_total_price() for item in cart_items)
#
#         # Prepare "product_name: quantity" string
#         product_name_quantity = ", ".join([f"{item.product.name}: {item.quantity}" for item in cart_items])
#         product_ids = ", ".join(f"{item.product.id}:x{item.quantity}" for item in cart_items
#         )
#
#         dummy_product = cart_items.first().product if cart_items.exists() else None
#         dummy_pharmacy = dummy_product.pharmacy if dummy_product else None
#
#         Purchase.objects.create(
#             patient=patient,
#             product=dummy_product,
#             quantity=product_name_quantity,  # Save product names and quantities as string here
#             payment_id=payment_id,
#             order_id=order_id,
#             total_amount=total,
#             pharmacy=dummy_pharmacy,
#             product_ids=product_ids,
#             status='pending'
#         )
#
#         cart_items.delete()
#         return render(request, 'cart/order_success.html/', {'order_id': order_id, 'total': total})
#
#     return redirect('cart')


@csrf_exempt
def complete_payment(request):
    if request.method != 'POST':
        return redirect('cart')

    # 1. Ensure a file is uploaded
    prescription = request.FILES.get('prescription_image')
    if not prescription:
        return render(request, 'cart/cart.html', {
            'error': 'Please upload a prescription image (JPEG/PNG).',
            **get_cart_context(request)
        })

    # 2. Validate extension using Django's validator
    validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
    try:
        validator(prescription)
    except ValidationError as e:
        return render(request, 'cart/cart.html', {
            'error': e.messages[0],
            **get_cart_context(request)
        })

    # 3. Validate file size (< 2 MB)
    if prescription.size > 2 * 1024 * 1024:
        return render(request, 'cart/cart.html', {
            'error': 'File too large — maximum allowed size is 2 MB.',
            **get_cart_context(request)
        })

    # 4. Process payment and save Purchase including the image
    payment_id = request.POST.get('razorpay_payment_id')
    order_id = request.session.get('razorpay_order_id')
    patient, session_key = get_patient_and_session(request)
    cart_items = CartItem.objects.filter(patient=patient, session_key=session_key)
    total = sum(item.get_total_price() for item in cart_items)

    product_summary = ", ".join(f"{item.product.name}: {item.quantity}" for item in cart_items)
    product_ids = ", ".join(f"{item.product.id}:x{item.quantity}" for item in cart_items)
    dummy = cart_items.first().product if cart_items.exists() else None

    Purchase.objects.create(
        patient=patient,
        product=dummy,
        quantity=product_summary,
        payment_id=payment_id,
        order_id=order_id,
        total_amount=total,
        pharmacy=dummy.pharmacy if dummy else None,
        product_ids=product_ids,
        prescription_image=prescription,
        status='pending'
    )

    cart_items.delete()
    return render(request, 'cart/order_success.html', {
        'order_id': order_id,
        'total': total
    })

def get_cart_context(request):
    patient, session_key = get_patient_and_session(request)
    cart_items = CartItem.objects.filter(patient=patient, session_key=session_key)
    total = sum(item.get_total_price() for item in cart_items)
    return {
        'cart_items': cart_items,
        'total': total,
        'razorpay_order_id': request.session.get('razorpay_order_id'),
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': total,
    }



def add_product(request):
    pha_id = request.session.get("uid")  # Pharmacy ID from session
    pharmacy = Pharmacy.objects.filter(pha_id=pha_id).first()

    if not pharmacy:
        return redirect('pharmacy_login')  # or handle error appropriately

    if request.method == 'POST':
        name = request.POST['name']
        brand = request.POST['brand']
        price = request.POST['price']
        description = request.POST['description']
        image = request.FILES.get('image')

        Product.objects.create(
            name=name,
            brand=brand,
            price=price,
            description=description,
            image=image,
            pharmacy=pharmacy
        )

        # Pass success message to the template
        return render(request, 'cart/product_add.html', {
            'msg': 'Product added successfully.'
        })

    return render(request, 'cart/product_add.html')



def medall(request):
    products = Product.objects.all()
    return render(request, 'cart/medall.html', {'products': products})