from rest_framework import serializers
from .models import Sale

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'date', 'product', 'category', 'amount']
