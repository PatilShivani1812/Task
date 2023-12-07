from datetime import timezone
from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['customer', 'order_date', 'address', 'order_items', 'order_number']

        def validate_order_date(self, value):
        # Add validation for order date not in the past
            if value < timezone.now().date():
                raise serializers.ValidationError("Order date cannot be in the past.")
            return value

    def validate(self, data):
        # Add validation for order cumulative weight under 150kg
        total_weight = sum(item['product'].weight * item['quantity'] for item in data['order_items'])
        if total_weight > 150:
            raise serializers.ValidationError("Order cumulative weight must be under 150kg.")
        
        return data
    


