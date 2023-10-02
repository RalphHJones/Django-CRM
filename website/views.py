from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddCustomerForm
from .models import Customer

# Create your views here.
def home(request):
    records = Customer.objects.all()



    #Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect("home")
        else:
            messages.success(request, "There was an error logging in, Please try again..." )
            return redirect("home")
    else:
        # messages.success(request, "Numb skull..." )
        return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect("home")

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # lookup record
        customer = get_object_or_404(Customer, id=pk)
        return render(request, 'customer.html', {'customer': customer})
    else:
        messages.success(request, "You need to log in first.")
        return redirect('home')
    
def delete_customer(request, pk):
    if request.user.is_authenticated:
        print (f"Deleting {pk}")
        cus = Customer.objects.get(id=pk)
        cus.delete()
        messages.success(request, "Customer has been deleted.")
        print ("Done deleting")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in.")
        return redirect('home')
        
def add_customer(request):
    form = AddCustomerForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_customer = form.save()
                messages.success(request, "Customer added.")
                return redirect('home')
        return render(request, 'add_customer.html', {'form': form})
    else:
        messages.success(request, "You need to be logged in.")
        return redirect('home')

def update_customer(request, pk):
    if request.user.is_authenticated:
        print (f"Updating {pk}")
        cus = Customer.objects.get(id=pk)
        form = AddCustomerForm(request.POST or None, instance=cus)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer has been updated.")
            print ("Done updating")
            return redirect('home')
        return render(request, 'update_customer.html', {'form': form})
    else:
        messages.success(request, "You need to be logged in.")
        return redirect('home')