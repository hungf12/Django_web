from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
import json
# change forms register django

# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cccd = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f'{self.user.username} - {self.cccd}'

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CreateUserForm(UserCreationForm):
    cccd = forms.CharField(max_length=12, label='CCCD')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'cccd']

    def clean_cccd(self):
        cccd = self.cleaned_data['cccd']
        if not cccd.isdigit() or len(cccd) != 12:
            raise forms.ValidationError("CCCD phải là số và đủ 12 chữ số.")
        if UserProfile.objects.filter(cccd=cccd).exists():
            raise forms.ValidationError("CCCD này đã được sử dụng.")
        return cccd

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, cccd=self.cleaned_data['cccd'])
        return user

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=256, null=True)
    attribute = models.CharField(max_length=256,null=True)
    # price = models.FloatField()
    price = models.DecimalField(max_digits=10,decimal_places=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=0,null=True,blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    storage_options = models.JSONField(default=dict)
    colors = models.JSONField(default=dict)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(null=False, blank=False, default=timezone.now)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=256, null=True)
    
    # Thêm các trường phục vụ MoMo
    momo_order_id = models.CharField(max_length=128, blank=True, null=True)
    momo_request_id = models.CharField(max_length=128, blank=True, null=True)
    momo_qr_code_url = models.URLField(blank=True, null=True)
    momo_pay_url = models.URLField(blank=True, null=True)
    momo_result_code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=256, null=True)
    city = models.CharField(max_length=256, null=True)
    phonenumber = models.CharField(max_length=256, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address    

class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()

    def __str__(self):
        return self.name
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    momo_order_id = models.CharField(max_length=150, unique=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    is_paid = models.BooleanField(default=False)
    method = models.CharField(
        max_length=50,
        choices=[('momo', 'MoMo'), ('cod', 'tiền mặt')],
        default='cod'
    )
    momo_trans_id = models.CharField(max_length=255, null=True, blank=True)  # <-- thêm dòng này
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order.id} - {'Đã thanh toán' if self.is_paid else 'Chưa thanh toán'}"
