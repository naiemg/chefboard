from rest_framework import serializers
from apps.menu.models import Restaurant, Category, MenuItem
from address.models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class RestaurantSerializer(serializers.ModelSerializer):        
    address = serializers.SerializerMethodField("get_addr")

    class Meta:
        model = Restaurant
        fields = ["id", "name", "address", "phone_number"]

    def get_addr(self, obj):
        return obj.address1.formatted

class CategorySerializer(serializers.ModelSerializer):
    # restaurant = RestaurantSerializer()
    
    class Meta:
        model = Category
        fields = "__all__"

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"