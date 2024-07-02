from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    retrieval_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
