from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import *
from django.db.models import Q
import json
from django .contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import uuid
import json
import hmac
import hashlib
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Payment
import time

from django.shortcuts import render, redirect
from .models import Order, OrderItem, Product, Payment
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CreateUserForm

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
            return redirect('login')
        else:
            messages.error(request, "Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.")
    else:
        form = CreateUserForm()
    
    context = {'form': form}
    return render(request, 'app/register.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'user or password not correct!')
    context ={}
    return render(request, 'app/login.html',context)
def logoutpage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'app/home.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    context = {'items': items,'order':order, 'cartItems': cartItems}
    return render(request, 'app/cart.html', context)

from django.contrib import messages  # để dùng thông báo
from django.shortcuts import redirect

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Order

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    if request.method == 'POST':
        selected_item_ids = request.POST.getlist('selected_items')

        if not selected_item_ids:
            messages.warning(request, "Vui lòng chọn ít nhất một sản phẩm để thanh toán.")
            return redirect('cart')

        items = order.orderitem_set.filter(id__in=selected_item_ids)
    else:
        items = order.orderitem_set.all()

    cart_total = sum([item.get_total for item in items])  # ✅ đã sửa
    cart_items = sum([item.quantity for item in items])

    context = {
        'items': items,
        'order': order,
        'cartItems': cart_items,
        'cartTotal': cart_total
    }
    return render(request, 'app/checkout.html', context)




def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer,complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product = product)
    if action =='add':
        orderItem.quantity +=1
    elif action =='remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('added', safe=False)
    # # cart_total =order.get_cart_items
    # # quantity =orderItem.quantity if orderItem.quantity > 0 else 0
    # # return JsonResponse({
    # #     'quantity': quantity,
    # #     'cart_total':cart_total
    # },safe=False)

def search_items(request):
    query = request.GET.get('q')
    result = []

    if query:
        query_name = f"Các dòng máy {query} hiện đang có"
        result = Product.objects.filter(Q(name__icontains=query))
    else:
        result = Product.objects.all()
        query_name = "Tất cả sản phẩm"
    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'results': result,
        "query": query,
        "query_name": query_name
    }

    return render(request, "app/search.html", context)

def intro(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    context = {'items': items,'order':order, 'cartItems': cartItems}
    return render(request, "app/intro.html",context)

def list_product(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']

    # Lọc sản phẩm dựa trên 'attribute'
    attribute = request.GET.get('attribute', 'all')
    if attribute == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(attribute=attribute)

    # Gộp tất cả biến vào một từ điển context
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'products': products  # Thêm products vào context
    }

    return render(request, 'app/list_product.html', context)


def contract(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order["get_cart_items"]
    
    # locations = Location.objects.all()

    context = {
        "items": items,
        "cartItems": cartItems,
        "order": order,
        # "locations": locations
    }
    return render(request, 'app/contract.html', context)

def product_detail(request, product_id):
    if request.user.is_authenticated:
       customer = request.user
       order, created = Order.objects.get_or_create(customer=customer, complete=False)
       items = order.orderitem_set.all()
       cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order["get_cart_items"]
    
    product = get_object_or_404(Product,id = product_id)

    context = {
        "items": items,
        "cartItems": cartItems,
        "order": order,
        "product": product
    }
    return render(request, 'app/product_detail.html', context)

def store_list(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order["get_cart_items"]
    
    stores = Store.objects.all()

    context = {
        "items": items,
        "cartItems": cartItems,
        "order": order,
        "stores": stores
    }
    
    return render(request, 'app/store_list.html',context)
    # stores = Store.objects.all()
    # return render(request, 'app/store_list.html', {'stores': stores}) 


def Transport(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    context = {'items': items,'order':order, 'cartItems': cartItems}
    return render(request, "app/transport.html",context)

def Guarantee(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    context = {'items': items,'order':order, 'cartItems': cartItems}
    return render(request, "app/guarantee.html",context)

def Payment_method(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    context = {'items': items,'order':order, 'cartItems': cartItems}
    return render(request, "app/payment_method.html",context)


# def create_order_view(request):
#     if request.method == "POST":
#         amount = int(request.POST["amount"])
#         order_id = str(uuid.uuid4())[:18]
#         payment = Payment.objects.create(order_id=order_id, amount=amount)
#         return redirect("payments:momo_create", order_id=order_id)
#     return render(request, "payments/create_order.html")

@login_required
def create_order_view(request):
    user = request.user
    try:
        order = Order.objects.get(customer=user, complete=False)
    except Order.DoesNotExist:
        return render(request, 'payments/create_order.html', {'message': 'Giỏ hàng trống!'})

    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_items')
        items = order.orderitem_set.filter(id__in=selected_ids)

        if not items.exists():
            return render(request, 'payments/create_order.html', {
                'message': 'Bạn chưa chọn sản phẩm nào!',
                'items': order.orderitem_set.all(),
                'order': order,
                'total': 0
            })

        total = sum(item.get_total for item in items)

        payment_method = request.POST.get('payment_method')

        # Đánh dấu đơn hàng là hoàn tất
        order.complete = True
        order.save()

        # Tạo thông tin thanh toán
        payment = Payment.objects.create(
            order=order,
            amount=total
        )

        # Lưu lại những item đã chọn bằng cách tạm thời giữ lại, xóa các item không chọn
        order.orderitem_set.exclude(id__in=selected_ids).delete()

        if payment_method == 'momo':
            return redirect('payments:momo_create', order_id=order.id)
        elif payment_method == 'vnpay':
            return redirect('payments:vnpay_create', order_id=order.id)
        else:
            return render(request, 'payments/create_order.html', {
                'message': 'Phương thức thanh toán không hợp lệ!',
                'items': items,
                'total': total,
                'order': order
            })

    else:
        # GET: hiển thị tất cả sản phẩm trong giỏ để người dùng chọn
        items = order.orderitem_set.all()
        total = sum(item.get_total for item in items)

    return render(request, 'payments/create_order.html', {
        'order': order,
        'items': items,
        'total': total
    })


from django.shortcuts import render, get_object_or_404
import uuid, time, hmac, hashlib, requests
from django.conf import settings
from .models import Payment
import qrcode
from io import BytesIO
import base64

def momo_create_payment(request, order_id):
    payment = get_object_or_404(Payment, order_id=order_id)
    request_id = str(uuid.uuid4())
    unique_order_id = f"{payment.order_id}_{int(time.time())}"

    # Lưu lại momo_order_id để đối chiếu về sau
    payment.momo_order_id = unique_order_id
    payment.save()

    raw_signature = (
        f"accessKey={settings.MOMO_ACCESS_KEY}"
        f"&amount={int(payment.amount)}"
        f"&extraData="
        f"&ipnUrl={settings.MOMO_NOTIFY_URL}"
        f"&orderId={unique_order_id}"
        f"&orderInfo=Thanh toán đơn hàng {payment.order_id}"
        f"&partnerCode={settings.MOMO_PARTNER_CODE}"
        f"&redirectUrl={settings.MOMO_RETURN_URL}"
        f"&requestId={request_id}"
        f"&requestType=captureWallet"
    )

    signature = hmac.new(
        settings.MOMO_SECRET_KEY.encode(),
        raw_signature.encode(),
        hashlib.sha256
    ).hexdigest()

    data = {
        "partnerCode": settings.MOMO_PARTNER_CODE,
        "accessKey": settings.MOMO_ACCESS_KEY,
        "requestId": request_id,
        "amount": str(int(payment.amount)),
        "orderId": unique_order_id,
        "orderInfo": f"Thanh toán đơn hàng {payment.order_id}",
        "redirectUrl": settings.MOMO_RETURN_URL,
        "ipnUrl": settings.MOMO_NOTIFY_URL,
        "extraData": "",
        "requestType": "captureWallet",
        "signature": signature,
        "lang": "vi"
    }

    response = requests.post(settings.MOMO_ENDPOINT, json=data)
    res_data = response.json()
    print("MoMo response:", response.status_code, res_data)

    if res_data.get("resultCode") != 0:
        return render(request, "payments/momo_qr.html", {
            "payUrl": "#",
            "qrCodeBase64": None,
            "message": f"Lỗi từ MoMo: {res_data.get('message')}"
        })

    # Lưu lại URL để sau này kiểm tra
    payment.momo_pay_url = res_data.get("payUrl")
    payment.save()

    # Tạo ảnh QR từ payUrl
    img = qrcode.make(res_data["payUrl"])
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "payments/momo_qr.html", {
        "payUrl": res_data["payUrl"],
        "qrCodeBase64": qr_code_base64,
        "message": "Vui lòng quét mã QR bằng ứng dụng MoMo để thanh toán."
    })



from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .models import Payment

@csrf_exempt
def momo_notify_view(request):
    if request.method != "POST":
        return HttpResponse("Phương thức không hợp lệ", status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse("Dữ liệu không hợp lệ", status=400)

    momo_order_id = data.get("orderId")
    result_code = data.get("resultCode")
    trans_id = data.get("transId")  # MoMo trả về transaction_id

    if not momo_order_id:
        return HttpResponse("Thiếu orderId", status=400)

    # Tìm payment theo momo_order_id
    payment = Payment.objects.filter(momo_order_id=momo_order_id).first()
    if not payment:
        return HttpResponse("Không tìm thấy đơn thanh toán", status=404)

    if result_code == 0:
        payment.is_paid = True
        payment.momo_trans_id = trans_id
        payment.save()

        # Có thể update thêm order.complete = True nếu cần:
        if payment.order:
            payment.order.complete = True
            payment.order.transaction_id = trans_id
            payment.order.save()

        return HttpResponse("Thanh toán thành công", status=200)

    # Nếu thanh toán thất bại hoặc bị hủy
    return HttpResponse("Thanh toán thất bại", status=400)


from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from app.models import Order, Payment

@login_required
def cod_payment_view(request):
    user = request.user
    try:
        order = Order.objects.get(customer=user, complete=False)
    except Order.DoesNotExist:
        return render(request, "payments/create_order.html", {"message": "Không tìm thấy đơn hàng!"})

    if order.orderitem_set.count() == 0:
        return render(request, "payments/create_order.html", {"message": "Giỏ hàng trống!"})

    total = order.get_cart_total()

    if request.method == "POST":
        # Hoàn tất đơn hàng và tạo payment
        order.complete = True
        order.save()

        Payment.objects.create(
            order=order,
            amount=total,
            method="cod",
            is_paid=False  # Tiền mặt nên chưa thanh toán
        )

        return render(request, "payments/success_cod.html", {"order": order})

    return render(request, "payments/confirm_cod.html", {"order": order, "total": total})


from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import hmac, hashlib
from app.models import Order, Payment

@login_required
def vnpay_create_payment(request, order_id):
    # order = get_object_or_404(Order, id=order_id, customer=request.user, complete=False)
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if order.orderitem_set.count() == 0:
        return render(request, "payments/create_order.html", {"message": "Giỏ hàng trống!"})

    total = int(order.get_cart_total)  # VNPay yêu cầu số nguyên

    # Đánh dấu hoàn tất đơn hàng
    order.complete = True
    order.save()

    # Tạo bản ghi thanh toán
    payment = Payment.objects.create(
        order=order,
        amount=total,
        method="vnpay",
        is_paid=False
    )

    txn_ref = f"{order.id}_{int(timezone.now().timestamp())}"

    vnp_params = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': settings.VNPAY_TMN_CODE,
        'vnp_Amount': str(total * 100),  # nhân 100
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': txn_ref,
        'vnp_OrderInfo': f"Thanh toán đơn hàng {order.id}",
        'vnp_OrderType': 'other',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': settings.VNPAY_RETURN_URL,
        'vnp_IpAddr': request.META.get('REMOTE_ADDR', '127.0.0.1'),
        'vnp_CreateDate': timezone.now().strftime('%Y%m%d%H%M%S'),
    }

    # Sắp xếp và tạo chữ ký
    sorted_params = sorted(vnp_params.items())
    query_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
    hash_data = '&'.join([f"{k}={v}" for k, v in sorted_params])
    secure_hash = hmac.new(
        settings.VNPAY_HASH_SECRET.encode('utf-8'),
        hash_data.encode('utf-8'),
        hashlib.sha512
    ).hexdigest()

    # URL thanh toán
    payment_url = f"{settings.VNPAY_URL}?{query_string}&vnp_SecureHash={secure_hash}"
    return redirect(payment_url)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def vnpay_return_view(request):
    params = request.GET
    vnp_TxnRef = params.get('vnp_TxnRef')
    vnp_ResponseCode = params.get('vnp_ResponseCode')

    order_id = vnp_TxnRef.split("_")[0]

    try:
        payment = Payment.objects.get(order__id=order_id, method='vnpay')
    except Payment.DoesNotExist:
        return render(request, 'payments/vnpay_fail.html', {"message": "Không tìm thấy giao dịch thanh toán."})

    if vnp_ResponseCode == '00':  # Thanh toán thành công
        payment.is_paid = True
        payment.save()
        return render(request, 'payments/vnpay_success.html', {"order_id": order_id})

    return render(request, 'payments/vnpay_fail.html', {"message": "Thanh toán thất bại."})
