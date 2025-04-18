from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from homemade.models import GlobalHomeMadeItem

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)

    def __str__(self):
        return self.name

# class Cart(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)

#     def __str__(self):
#         return f"{self.item.name} - {self.quantity}"
from homemade.models import HomeMadeItem

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(HomeMadeItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"

    @property
    def subtotal(self):
        return self.item.price * self.quantity

# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     total = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"Order #{self.id} by {self.user}"
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField(blank=True, null=True)  # ✅ NEW FIELD

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     item = models.ForeignKey(HomeMadeItem, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)


#     def __str__(self):
#         return f"{self.quantity} x {self.item.item}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(HomeMadeItem, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.item if self.item else '[Deleted Item]'}"
    @property
    def subtotal(self):
        return self.price * self.quantity
