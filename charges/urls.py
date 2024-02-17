from django.urls import path
from . import views

urlpatterns = [
    path('sellers/', views.list_sellers),
    path('costumers/', views.list_costumers),
    path('addseller/', views.add_seller),
    path('addcostumer/', views.add_costumer),
    path('sellerincrease/', views.charge_seller),
    path('sell/', views.transaction),
    path('deleteseller/', views.delete_seller),
    path('deletecostumer/', views.delete_costumer),
    path('sellers/<str:username>', views.seller_details),
    path('costumers/<str:phone_number>', views.costumer_details),
]
