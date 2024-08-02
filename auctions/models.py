from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=32)

    def __str__(self):
        return self.category_name

class Bid(models.Model):
    bid = models.DecimalField(max_digits=6, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user_bid")

    def __str__(self):
        return str(self.bid)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=280)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=False, related_name="cost")
    image = models.URLField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="type")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user_sell")
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="list")

    def __str__(self):
        return self.title

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="item")
    comment = models.CharField(max_length=140)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user_comment")

    def __str__(self):
        return f"{self.commenter} commented on {self.listing}"
