from multiprocessing import context
from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import authenticate,login,logout 
from .form import Orderform,CreateUserForm,CustomerForm
from .filters import Orderfilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user , allowed_users , admin_only
# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            user = form.save()
            username = form.cleaned_data.get('username')
           
        
            messages.success(request,'Account has been created for' + username)
            return redirect('login')
    context = {'form':form}
    return render(request,'register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            
            login(request,user)
            return redirect('home')
            
        else:
            messages.info(request,'Username or password is incorrect')

    context = {}
    return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

    
@login_required(login_url='login')
@admin_only
def home(request):
    orders  = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders,'customers':customers,'total_customers':total_customers,'total_orders':total_orders,
    'delivered':delivered,'pending':pending}
    return render(request,'dashboard.html',context)

  


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    print(orders)
    context = {'orders':orders,'total_orders':total_orders,
    'delivered':delivered,'pending':pending}
    return render(request,'user.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
            form = CustomerForm(request.POST,request.FILES,instance=customer)
            if form.is_valid:
                form.save()
    context ={'form':form}
    return render(request,'accounts_settings.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Products.objects.all()
    return render(request,'products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()

    myfilter =Orderfilter(request.GET,queryset=orders)
    orders = myfilter.qs
    context = {'customer':customer,'orders':orders,'orders_count':orders_count,'myfilter':myfilter}

    return render(request,'customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=20)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = Orderform(initial={'customer':customer})
    if request.method == 'POST':
        # form = Orderform(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request,'order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = Orderform(instance=order)
    if request.method == 'POST':
        form = Orderform(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'order_form.html',context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):

    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context ={'item':order}
    return render(request,'delete.html',context)

