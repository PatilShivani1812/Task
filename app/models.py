from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(25)])  # Add appropriate validators



class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=15, unique=True,editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)
    order_items = models.ManyToManyField('OrderItem', related_name='order_items')

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.all().order_by('-id').first()
            if last_order:
                last_number = int(last_order.order_number[3:])  # Extract numeric part
                new_number = last_number + 1
            else:
                new_number = 1

            self.order_number = f"ORD{new_number:05d}"

        super().save(*args, **kwargs)

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()



from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(25)])

class Order(models.Model):
    order_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # Add other fields as needed

    def get_cumulative_weight(self):
        return sum(item.product.weight * item.quantity for item in self.order_items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        # Validation: Customer's name must be unique
        validators = [
            serializers.UniqueValidator(queryset=Customer.objects.all(), message="Customer with this name already exists.")
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # Validation: Product's name must be unique
        validators = [
            serializers.UniqueValidator(queryset=Product.objects.all(), message="Product with this name already exists.")
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    # Validation: Order cumulative weight must be under 150kg
    def validate_order_items(self, value):
        total_weight = sum(item.product.weight * item.quantity for item in value)
        if total_weight > 150:
            raise serializers.ValidationError("Order cumulative weight must be under 150kg.")
        return value

    # Validation: Order Date cannot be in the past
    def validate_order_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Order Date cannot be in the past.")
        return value
