from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import *
from django.db.models import Q
import json
from django .contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context ={'form':form}
    return render(request, 'app/register.html',context)
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
def checkout(request):
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
        query_name = f"kết quả trả về cho sản phẩm {query}"
        result = Product.objects.filter(Q(name__icontains=query))[:1]
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