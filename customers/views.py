from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                     CreateAPIView, RetrieveAPIView, ListAPIView)
from rest_framework.views import APIView

from .models import Customer, Payment
from .serializers import (CustomerSerializer, PaymentSerializer, )
from .pagination import StandardResultsSetPagination
from .permissions import IsCustomStaff


class ListCreateCustomerView(ListCreateAPIView):
    """View to list services"""

    permission_classes = [IsCustomStaff]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "success", "data": serializer.data},
                            status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyCustomerView(RetrieveUpdateDestroyAPIView):
    """Get, update or delete a single customer"""

    permission_classes = [IsCustomStaff]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    http_method_names = ['get', 'patch', 'delete', ]
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({"status": "success", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCustomerPaymentView(CreateAPIView):
    """View to create customer payment"""

    permission_classes = [IsCustomStaff]
    serializer_class = PaymentSerializer

    def create(self, request, customer_slug, *args, **kwargs):
        customer = get_object_or_404(Customer, slug=customer_slug)
        serializer = self.serializer_class(customer=customer, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(customer=customer)
            return Response({"status": "success", "data": serializer.data},
                            status=status.HTTP_201_CREATED)


class GetSingleCustomerPaymentView(RetrieveAPIView):
    """View to get single customer payment"""

    permission_classes = [IsCustomStaff]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ['get', ]
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetMultipleCustomerPaymentView(ListAPIView):
    """View to get multiple customer payment"""

    permission_classes = [IsCustomStaff]
    serializer_class = PaymentSerializer
    http_method_names = ['get', ]

    def get_queryset(self):
        customer = get_object_or_404(Customer, slug=self.kwargs.get("customer_slug"))
        return customer.payments.all()


class GetAllPaymentView(ListAPIView):
    """View to get all customer payments"""

    permission_classes = [IsCustomStaff]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', ]


class SearchView(APIView):
    """Search view. """

    permission_classes = [IsCustomStaff]

    def get(self, request, *args, **kwargs):

        query = request.query_params.get("query")
        if query:
            customer = Customer.objects.filter(
                Q(name__icontains=query)
                | Q(email__iexact=query)).distinct()
            serializer = CustomerSerializer(customer, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Something went wrong. Try again."},
                            status=status.HTTP_400_BAD_REQUEST)
