from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    like_counts = models.IntegerField(default=0)
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_product')

class Likes(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_likes')

    class Meta:
        unique_together= (('user', 'product'),) # this will make both the user and product a composite key 

class Cart(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart', )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cart')
    quantity = models.IntegerField()
    total_price= models.FloatField()
