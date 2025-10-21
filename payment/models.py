from django.db import models
from django.contrib.auth.models import User

class RazorpayPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    amount = models.IntegerField()  # in paise
    payment_id = models.CharField(max_length=100, blank=True)
    order_id = models.CharField(max_length=100)
    signature = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username if self.user else 'Guest'} - ₹{self.amount/100} - {'Paid' if self.paid else 'Pending'}"
