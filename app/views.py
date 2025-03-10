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
    # if request.method == "POST":
    #     searched = request.POST["searched"]
    #     keys = Product.objects.filter(name__contains = searched)
    # return render(request, "app/search.html", {"searched": searched, "keys": keys})
    query = request.GET.get('q')
    result = []

    if query:
        result = Product.objects.filter(Q(name__icontains=query))[:1]
    else:
        result = Product.objects.all()

    return render(request, "app/search.html", {"results": result, "query": query})

def intro(request):
    return render(request, "app/intro.html")

def list_product(request):
    attribute = request.GET.get('attribute','all')
    if attribute == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(attribute=attribute)
    return render(request,'app/list_product.html',{'products':products})

def contract(request):
    # Location.objects.create(location_name="default", latitude=10.762622, longitude=106.660172)
    locations = Location.objects.all()
    return render(request, 'app/contract.html',{'locations':locations})

def product_detail(request, product_id):
    product = get_object_or_404(Product,id = product_id)
    return render(request, 'app/product_detail.html', {'product': product})