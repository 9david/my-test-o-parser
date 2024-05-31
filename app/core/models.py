"""
Database models
"""

from django.db import models

class Product(models.Model):
    """Product object."""
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField(max_length=255)
    image_url = models.URLField(max_length=255)
    discount = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id) + ' ' + self.name
