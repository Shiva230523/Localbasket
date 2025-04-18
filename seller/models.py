# from django.db import models
# from django.conf import settings

# class SellerItem(models.Model):
#     seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_items')
#     item = models.CharField(max_length=50)
#     price = models.FloatField()
#     address = models.TextField(default='')

#     def __str__(self):
#         return f"{self.item} by {self.seller.first_name}"

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         # Update or create LocalItem
#         local_item, created = LocalItem.objects.get_or_create(
#             seller=self.seller,
#             item=self.item,
#             defaults={'price': self.price, 'address': self.address}
#         )
#         if not created:
#             local_item.price = self.price
#             local_item.address = self.address
#             local_item.save()

#     def delete(self, *args, **kwargs):
#         LocalItem.objects.filter(seller=self.seller, item=self.item).delete()
#         super().delete(*args, **kwargs)

# class LocalItem(models.Model):
#     seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     item = models.CharField(max_length=50)
#     price = models.FloatField()
#     address = models.TextField()

#     def __str__(self):
#         return self.item

# class DealItem(models.Model):
#     seller_item = models.ForeignKey(SellerItem, on_delete=models.CASCADE, related_name='deal_items')
#     deal_price = models.FloatField()
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.seller_item.item} on Deal"
from django.db import models
from django.conf import settings

class SellerItem(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_items')
    item = models.CharField(max_length=50)
    price = models.FloatField()
    address = models.TextField(default='')
    image = models.ImageField(upload_to='seller_item_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.item} by {self.seller.first_name}"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        local_item, created = LocalItem.objects.get_or_create(
            seller=self.seller,
            item=self.item,
            defaults={
                'price': self.price,
                'address': self.address,
                'image': self.image  # NEW
        }
    )
        if not created:
            local_item.price = self.price
            local_item.address = self.address
            local_item.image = self.image  # NEW
            local_item.save()
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     local_item, created = LocalItem.objects.get_or_create(
    #         seller=self.seller,
    #         item=self.item,
    #         defaults={'price': self.price, 'address': self.address}
    #     )
    #     if not created:
    #         local_item.price = self.price
    #         local_item.address = self.address
    #         local_item.save()

    def delete(self, *args, **kwargs):
        LocalItem.objects.filter(seller=self.seller, item=self.item).delete()
        super().delete()

# class LocalItem(models.Model):
#     seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     item = models.CharField(max_length=50)
#     price = models.FloatField()
#     address = models.TextField()

#     def __str__(self):
#         return self.item
class LocalItem(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.CharField(max_length=50)
    price = models.FloatField()
    address = models.TextField()
    image = models.ImageField(upload_to='local_item_images/', null=True, blank=True)  # NEW

    def __str__(self):
        return self.item



class DealItem(models.Model):
    seller_item = models.ForeignKey(SellerItem, on_delete=models.CASCADE, related_name='deal_items')
    deal_price = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seller_item.item} on Deal"
