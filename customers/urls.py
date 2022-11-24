from django.urls import path, include

from .views import (ListCreateCustomerView, RetrieveUpdateDestroyCustomerView,
                    CreateCustomerPaymentView, GetSingleCustomerPaymentView,
                    GetMultipleCustomerPaymentView, GetAllPaymentView, SearchView)

urlpatterns = [
    path('customer/', ListCreateCustomerView.as_view(), name="customer"),
    path('customer/<str:slug>/', RetrieveUpdateDestroyCustomerView.as_view(), name="customer_detail"),
    path('customer-payment/<str:customer_slug>/', CreateCustomerPaymentView.as_view(),
         name="customer_payment"),
    path('customer-payment-detail/<str:slug>/', GetSingleCustomerPaymentView.as_view(),
         name="customer_payment_detail"),
    path('customer-payment-multiple/<str:customer_slug>/', GetMultipleCustomerPaymentView.as_view(),
         name="customer_payment_multiple"),
    path('customer-payments/', GetAllPaymentView.as_view(),
         name="customer_payments"),
    path("search", SearchView.as_view(), name="search"),

]
