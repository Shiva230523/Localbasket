from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class GlobalHomeMadeItem(models.Model):
    homemade_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='global_homemade_items')
    item = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    address = models.TextField()
    image = models.ImageField(upload_to='global_homemade_items/', null=True, blank=True)

    def __str__(self):
        return self.item

# class HomeMadeItem(models.Model):
#     homemade_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='homemade_items')
#     item = models.CharField(max_length=50)
#     price = models.FloatField()
#     address = models.TextField()
#     image = models.ImageField(upload_to='homemade_items/', null=True, blank=True)

#     def __str__(self):
#         return f"{self.item} by {self.homemade_user.first_name}"

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         global_item, created = GlobalHomeMadeItem.objects.get_or_create(
#             homemade_user=self.homemade_user,
#             item=self.item,
#             defaults={
#                 'price': self.price,
#                 'address': self.address,
#                 'image': self.image,
#             }
#         )
#         if not created:
#             global_item.price = self.price
#             global_item.address = self.address
#             if self.image:
#                 global_item.image = self.image
#             global_item.save()

#     def delete(self, *args, **kwargs):
#         GlobalHomeMadeItem.objects.filter(homemade_user=self.homemade_user, item=self.item).delete()
#         super().delete(*args, **kwargs)
class HomeMadeItem(models.Model):
    homemade_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='homemade_items')
    item = models.CharField(max_length=50)
    price = models.FloatField()
    address = models.TextField()
    image = models.ImageField(upload_to='homemade_items/', null=True, blank=True)
    order_limit = models.PositiveIntegerField(default=10)  # ✅ new field
    order_count = models.PositiveIntegerField(default=0)   # ✅ new field

    def __str__(self):
        return f"{self.item} by {self.homemade_user.first_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        global_item, created = GlobalHomeMadeItem.objects.get_or_create(
            homemade_user=self.homemade_user,
            item=self.item,
            defaults={
                'price': self.price,
                'address': self.address,
                'image': self.image,
            }
        )
        if not created:
            global_item.price = self.price
            global_item.address = self.address
            if self.image:
                global_item.image = self.image
            global_item.save()

    def delete(self, *args, **kwargs):
        GlobalHomeMadeItem.objects.filter(homemade_user=self.homemade_user, item=self.item).delete()
        super().delete(*args, **kwargs)
