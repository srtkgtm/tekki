from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    
    def get_retrieval_count(self, object):
        return object.retrieval_count
    
    def get_time_period(self, object):
        return object.time_period

    class Meta:
        model = Product
        fields = '__all__'



