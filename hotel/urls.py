from django.urls import path
from . import views


app_name = 'hotel'

urlpatterns = [
  path("", views.index, name="index"),
  path("sign_up/", views.sign_up, name="sign_up"),
  path("logout", views.logout_user, name="logout"),
  path("login", views.login_user, name="login"),
  path("nutrient/create", views.nutrient_create, name="nutrient_create"),
  path('nutrients_list',views.nutrients_list, name= "nutrients_list"),
  path('nutrient/edit/<int:id>', views.nutrient_edit, name="nutrient_edit"),
  path('nutrient/delete/<int:id>', views.nutrient_destroy, name="nutrient_destroy"),
  path('product/new', views.product_create, name='product_create'),
  path('products_list',views.products_list, name= "products_list"),
  path('product/edit/<int:id>', views.product_edit, name="product_edit"),
  path('product/delete/<int:id>', views.product_destroy, name="product_destroy"),
]