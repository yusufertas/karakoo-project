from rest_framework import serializers

from customer.models import Customer, User, Log, CustomerContact


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')


class CustomerContactSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=256)
    last_name = serializers.CharField(max_length=256)
    phone = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField()

    class Meta:
        model = CustomerContact
        fields = ('user_id', 'first_name', 'last_name', 'email', 'phone')


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=256)
    last_name = serializers.CharField(max_length=256)
    phone = serializers.CharField(max_length=20, required=False)
    company = serializers.CharField(max_length=256, required=False)
    email = serializers.EmailField(max_length=256, required=False)
    reference = serializers.CharField(max_length=256, required=False)

    class Meta:
        model = Customer
        fields = ('user_id', 'first_name', 'last_name', 'phone', 'company', 'email', 'reference',)


class LogSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    log = serializers.CharField()

    class Meta:
        model = Log
        fields = ('user_id', 'customer_id', 'log',)
