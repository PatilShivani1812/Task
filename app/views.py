from django.shortcuts import render
from requests import Response
from rest_framework import generics
from .models import Customer, Product, Order, OrderItem
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from rest_framework import status
from .serializers import OrderItemSerializer
# Create your views here.

class CustomerListCreateView(generics.ListCreateAPIView):
    """List and create view for Customers.

    This view allows listing all existing Customers and creating new Customer instances.
    Returns:
    Response: Returns a Response object containing the serialized list of Customers or indicating the success or
    failure of the creation operation."""
   
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and destroy view for Customers.
    This view allows retrieving, updating, and deleting Customer instances.
    Returns:
    Response: Returns a Response object containing the serialized Customer data or indicating the success or failure
    of the update or deletion operation."""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    """List and create view for Products.
    This view allows listing all existing Products and creating new Products.    
    Returns:
    Response: Returns a Response object containing a list of Products or indicating the success or failure of the
    creation operation."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and destroy view for Products.
    This view allows retrieving, updating, and deleting a specific Product.
    Returns:
    Response: Returns a Response object containing Product details or indicating the success or failure of the
    update or delete operation."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    """List and create view for Orders.
    This view allows the listing of all Orders and the creation of new Orders.
    Returns:
    Response: Returns a Response object containing the list of Orders or indicating the success or failure of the
    Order creation operation."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detail view for Orders.
    This view allows the retrieval, updating, and deletion of individual Orders based on their unique identifier.
    Returns:
    Response: Returns a Response object containing the details of the Order or indicating the success or failure
    of the update or deletion operation."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detail view for OrderItems.
    This view allows the retrieval, updating, and deletion of individual OrderItems based on their unique identifier.
    Returns:
    Response: Returns a Response object containing the details of the OrderItem or indicating the success or failure
    of the update or deletion operation.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderItemCreateView(generics.CreateAPIView):
    """  Create view for OrderItems.

    This view allows the creation of OrderItems by providing the necessary data in the request payload.
    The 'order' field is a required field, and the associated Order must exist for the OrderItem to be created.
    Returns:
    Response: Returns a Response object indicating the success or failure of the OrderItem creation.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def perform_create(self, serializer):
        """
        Override the default perform_create method to ensure that the 'order' field is set before saving the OrderItem.
        Returns:       
        Response: Returns a Response object indicating the success or failure of the OrderItem creation.
         """
        order_id = self.request.data.get('order')
        
        if not order_id:
            return Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order with the specified ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(order=order)





