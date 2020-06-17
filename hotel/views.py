from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.urls import reverse

from .models import Nutrient, Product ,ProductNutrients
from .form import NutrientForm, ProductForm, ProductNutrientsForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView




# Create your views here.
def index(request):
  return render(request = request,
                template_name='hotel/index.html',
                context = {"nutrients":Nutrient.objects.all})


def sign_up(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f"New account created: {username}")
      login(request, user)
      return redirect("hotel:index")
    else:
      for msg in form.error_messages:
        print(form.error_messages[msg])
        messages.error(request, f"{msg}: {form.error_messages[msg]}")

      return render(request=request,
                    template_name="hotel/sign_up.html",
                    context={"form": form})

  form = UserCreationForm
  return render(request = request,
                template_name = "hotel/sign_up.html",
                context={"form":form})


def login_user(request):
  if request.method == 'POST':
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        messages.info(request, f"You are now logged in as {username}")
        return redirect('/')
      else:
        messages.error(request, "Invalid username or password.")
    else:
      messages.error(request, "Invalid username or password.")
  form = AuthenticationForm()
  return render(request=request,
                template_name="hotel/login.html",
                context={"form": form})

def logout_user(request):
  logout(request)
  messages.info(request, "Logged out successfully!")
  return redirect("hotel:index")

def nutrient_create(request):
  if request.method == 'POST':
    context = {}
    # create object of form
    form = NutrientForm(request.POST or None)
    # check if form data is valid
    if form.is_valid():
      # save the form data to model
      fs = form.save(commit=False)
      fs.updated_by = request.user
      fs.save()
      messages.info(request, f"Nutrient {form.cleaned_data['nutrient_name']} is created.")
      return redirect('/')
    else:
      messages.error(request, "Invalid details")

  form = NutrientForm
  return render(request=request,
                template_name="hotel/nutrient_create.html",
                context={"form": form})

def nutrients_list(request):
    nutrients = Nutrient.objects.all()
    return render(request, "hotel/nutrients_list.html", {'nutrients': nutrients})


def nutrient_edit(request, id):
  if not request.user.is_authenticated:
    messages.info(request, "Please Login to continue.")
    return redirect('/')
  nutrient = Nutrient.objects.get(pk=id)
  if request.method == "GET":
    return render(request, "hotel/nutrient_edit.html", {'nutrient': nutrient})
  else:
    form = NutrientForm(request.POST or None, instance=nutrient)
    if form.is_valid():
      fs = form.save(commit=False)
      fs.updated_by = request.user
      fs.save()
      messages.info(request, f"Nutrient {nutrient.nutrient_name} is updated.")
      return redirect('hotel:nutrients_list')
    return render(request, 'hotel/nutrient_edit.html', {'nutrient': nutrient})


def nutrient_destroy(request, id):
  if not request.user.is_authenticated:
    messages.info(request, "Please Login to continue.")
    return redirect('/')
  nutrient = Nutrient.objects.get(id=id)
  nutrient.delete()
  messages.info(request, f"Nutrient {nutrient.nutrient_name} is deleted.")
  return redirect('hotel:nutrients_list')

def product_create(request):
  if not request.user.is_authenticated:
    messages.info(request, "Please Login to continue.")
    return redirect('/')
  if request.method == 'POST':
    # context = {}
    # # create object of form
    form = ProductForm(request.POST or None)
    product = Product(name= form.data['name'], description= form.data['description'])
    if form.data['status'] == 'True':
      product.status = True
    else:
      product.status = False
    try:
      product.save()
      i = 0
      value = True
      while value:
        pn= ProductNutrients(product=product,nutrient=Nutrient(pk=request.POST[f"basic_attributes[{i}][select]"]),nutrient_value=request.POST[f"basic_attributes[{i}][number]"],updated_by=request.user)
        pn.save()
        i += 1
        try:
          value = request.POST[f"basic_attributes[{i}][select]"]
        except :
          value = False
      messages.info(request, f"Product {form.data['name']} is created.")
      return redirect('/')
    except:
      messages.error(request, "Invalid details")
      return redirect('/')
  else:
    nutrients = Nutrient.objects.all()
    product_form = ProductForm()
    context = {'product_form': product_form, 'nutrients': nutrients}
    return render(request=request,
                  template_name="hotel/product_create.html",
                  context=context)


def products_list(request):
  products = Product.objects.all()
  nutrients ={}
  for product in products:
    nutrients[product.pk] = product.productnutrients_set.all()
  return render(request, "hotel/products_list.html", {'products': products, 'nutrients': nutrients})

def product_edit(request, id):
  if not request.user.is_authenticated:
    messages.info(request, "Please Login to continue.")
    return redirect('/')
  product = Product.objects.get(pk=id)
  product_nutrients= product.productnutrients_set.all()
  nutrients = Nutrient.objects.all()
  if request.method == "GET":
    return render(request, "hotel/product_edit.html", {'product': product, 'product_nutrients': product_nutrients, 'nutrients': nutrients})
  else:
    form = ProductForm(request.POST or None)
    Product.objects.filter(pk=id).update(name=form.data['name'], description=form.data['description'])
    if form.data['status'] == 'True':
      product.status = True
    else:
      product.status = False
    try:
      i = 0
      value = True
      updated = {}
      while value:
        try:
          n_id = request.POST[f"nutrient[{i}][id]"]
          pn = ProductNutrients.objects.get(pk=n_id)
        except:
          n_id = False

        if not n_id:
          pn = ProductNutrients(product=product, nutrient=Nutrient(pk=request.POST[f"basic_attributes[{i}][select]"]),
                                nutrient_value=request.POST[f"basic_attributes[{i}][number]"], updated_by=request.user)
          pn.save()
        else:
          updated[pn.pk] = True
          ProductNutrients.objects.filter(pk=n_id).update(nutrient=Nutrient(pk=request.POST[f"basic_attributes[{i}][select]"]),nutrient_value=request.POST[f"basic_attributes[{i}][number]"],updated_by=request.user)
        i += 1
        try:
          value = request.POST[f"basic_attributes[{i}][select]"]
        except :
          value = False
      messages.info(request, f"Product {form.data['name']} is updated.")
      return redirect('/')
    except:
      messages.error(request, "Invalid details")
    return render(request, "hotel/product_edit.html", {'product': product, 'product_nutrients': product_nutrients, 'nutrients': nutrients})


def product_destroy(request, id):
  if not request.user.is_authenticated:
    messages.info(request, "Please Login to continue.")
    return redirect('/')
  product = Product.objects.get(pk=id)
  product.delete()
  messages.info(request, f"Product {product.name} is deleted.")
  return redirect('hotel:products_list')