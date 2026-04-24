from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileEditForm, ProductForm
from django.contrib.auth.decorators import login_required

# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# View Products by Category
def category(request, key):
    key = key.replace('-', ' ')
    try:
        category = Category.objects.get(name=key)
        products = Product.objects.filter(category=category)
        categories = Category.objects.all()
        return render(request, 'category.html', {'products': products, 'category': category, 'categories': categories})
    except Category.DoesNotExist:
        messages.error(request, "Oops! Category does not exist.")
        return redirect('home')

# View Individual Product
def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product.html', {'product': product})

# About Page
def about(request):
    return render(request, 'about.html', {})

# User Login
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Handle superuser login
            if user.is_superuser:
                messages.success(request, "Logged In Successfully!")
                return redirect('home')
            try:
                Customer.objects.get(email=user.email)  # Removed role handling
                return redirect('home')
            except Customer.DoesNotExist:
                messages.error(request, "Customer profile not found. Please contact support.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    return render(request, 'login.html', {})

# User Logout
def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')

# User Registration
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            Customer.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone="",  # Removed role field
                password=password,
            )
            messages.success(request, "User Registered Successfully!")
            return redirect('home')
        else:
            messages.error(request, "User Registration Failed. Please Try Again!")
            return redirect('register')
    return render(request, 'register.html', {'form': form})

# Add Product
@login_required
def add_product(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = ProductForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Product Added Successfully!")
                    return redirect('home')
            else:
                form = ProductForm()
            return render(request, 'add_product.html', {'form': form})
        else:
            customer = get_object_or_404(Customer, email=request.user.email)
            if request.method == 'POST':
                form = ProductForm(request.POST, request.FILES)
                if form.is_valid():
                    product = form.save(commit=False)
                    product.seller = customer
                    product.save()
                    messages.success(request, "Product Added Successfully!")
                    return redirect('home')
            else:
                form = ProductForm()
            return render(request, 'add_product.html', {'form': form})
    messages.error(request, "Access Denied!")
    return redirect('login')

# Edit Product
@login_required
def edit_product(request, pk):
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product Updated Successfully!")
                return redirect('product_list')
        else:
            form = ProductForm(instance=product)
        return render(request, 'edit_product.html', {'form': form, 'product': product})
    messages.error(request, "Access Denied!")
    return redirect('login')

# View All Products
@login_required
def product_list(request):
    if request.user.is_superuser:
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})
    messages.error(request, "Access Denied!")
    return redirect('home')

# Delete Product
@login_required
def delete_product(request, pk):
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=pk)
        if request.method == 'POST':
            product.delete()
            messages.success(request, "Product Deleted Successfully!")
            return redirect('product_list')
        return render(request, 'delete_product.html', {'product': product})
    messages.error(request, "Access Denied!")
    return redirect('home')

# Edit User Profile
def edit_profile(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, email=request.user.email)
        if request.method == 'POST':
            form = ProfileEditForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile Updated Successfully!")
                return redirect('home')
        else:
            form = ProfileEditForm(instance=customer)
        return render(request, 'edit_profile.html', {'form': form})
    return redirect('login')
