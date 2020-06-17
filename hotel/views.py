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
  nutrient = Nutrient.objects.get(pk=id)
  if request.method == "GET":
    return render(request, "hotel/nutrient_edit.html", {'nutrient': nutrient})
  else:
    # import pdb; pdb.set_trace()
    form = NutrientForm(request.POST or None, instance=nutrient)
    if form.is_valid():
      fs = form.save(commit=False)
      fs.updated_by = request.user
      fs.save()
      messages.info(request, f"Nutrient {nutrient.nutrient_name} is updated.")
      return redirect('hotel:nutrients_list')
    return render(request, 'hotel/nutrient_edit.html', {'nutrient': nutrient})


def nutrient_destroy(request, id):
  nutrient = Nutrient.objects.get(id=id)
  nutrient.delete()
  messages.info(request, f"Nutrient {nutrient.nutrient_name} is deleted.")
  return redirect('hotel:nutrients_list')

def product_create(request):
  if request.method == 'POST':
    # context = {}
    # # create object of form
    form = ProductForm(request.POST or None)
    # # check if form data is valid
    # if form.is_valid():
    #   # save the form data to model
    #   fs = form.save(commit=False)
    #   fs.updated_by = request.user
    #   fs.save()
    #   messages.info(request, f"Nutrient {form.cleaned_data['nutrient_name']} is created.")
    #   return redirect('/')
    # else:
    #   messages.error(request, "Invalid details")
  else:
    nutrients = Nutrient.objects.all()
    product_form = ProductForm()
    product_nutrients = ProductNutrientsForm()
    context = {'product_nutrients': product_nutrients, 'product_form': product_form}
    return render(request=request,
                  template_name="hotel/product_create.html",
                  context=context)

def products_list(request):
  products = Product.objects.all()
  nutrients ={}
  for product in products:
    nutrients[product.pk] = product.productnutrients_set.all()
  # import pdb; pdb.set_trace()
  return render(request, "hotel/products_list.html", {'products': products, 'nutrients': nutrients})

# class ParentListView(ListView):
#   model = Parent
#
#
# class ProductCreateView(CreateView):
#   model = Product
#   fields = ["name","description","status"]
#
#   def get_context_data(self, **kwargs):
#     data = super().get_context_data(**kwargs)
#     if self.request.POST:
#       data["product_nutrients"] = ProductNutrientFormset(self.request.POST)
#     else:
#       data["product_nutrients"] = ProductNutrientFormset()
#     return data
#
#   def form_valid(self, form):
#     context = self.get_context_data()
#     product_nutrients = context["product_nutrients"]
#     self.object = form.save()
#     if product_nutrients.is_valid():
#       product_nutrients.instance = self.object
#       product_nutrients.save()
#     return super().form_valid(form)
#
#
#   def get_success_url(self):
#     return reverse("hotel:product_list")