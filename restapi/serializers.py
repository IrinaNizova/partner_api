from rest_framework import serializers
from rest_framework import mixins
from rest_framework import generics

from .models import ReuqestToCredit, CustomerProfile

class CreditRequestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReuqestToCredit
        fields = '__all__'


class CustomerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = '__all__'

