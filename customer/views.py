from django.http import JsonResponse
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, ListModelMixin, \
    CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from customer.models import User, Customer, Log, CustomerContact
from customer.permissions import IsOwner
from customer.serializers import UserSerializer, CustomerSerializer, LogSerializer, CustomerContactSerializer


class UserViewSet(GenericViewSet,
                  CreateModelMixin,
                  RetrieveModelMixin,
                  ListModelMixin,
                  UpdateModelMixin):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer


class CustomerContactViewSet(GenericViewSet,
                          CreateModelMixin):
    queryset = CustomerContact.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = CustomerContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.id == serializer.validated_data['user_id']:
            obj = CustomerContact.objects.create(**serializer.data)
            obj.user = request.user
            obj.save()
            return JsonResponse(serializer.data)
        return JsonResponse({"detail": "Invalid user selection"}, status=403)


class CustomerViewSet(GenericViewSet,
                      CreateModelMixin,
                      RetrieveModelMixin,
                      ListModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin):
    queryset = Customer.objects.prefetch_related('user').all()
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.id == serializer.validated_data['user_id']:
            obj = Customer.objects.create(**serializer.data)
            obj.user = request.user
            obj.save()

            #Update the customer_contact to customer object:
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            customer_contact = CustomerContact.objects.get(first_name=first_name,
                                                           last_name=last_name,
                                                           email=email)
            customer_contact.customer = obj
            customer_contact.save()
            return JsonResponse(serializer.validated_data)
        else:
            return JsonResponse({"detail": "Invalid user selection"}, status=403)

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return Response(super().list(request).data)
        qs = self.get_queryset()
        customer_list = list(qs.filter(user=request.user))
        serializer = CustomerSerializer(customer_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return Response(super().retrieve(request).data)
        customer = self.get_object()
        serializer = CustomerSerializer(customer)
        return JsonResponse(serializer.data, safe=False)

    def update(self, request, *args, **kwargs):
        if request.user.id == int(kwargs['pk']) or request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            #Update the customer contact table as well

            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data.get('email')
            phone = serializer.validated_data.get('phone')
            related_customer = CustomerContact.objects.filter(customer__id=int(kwargs['pk']))
            related_customer.update(
                first_name=first_name,
                last_name=last_name,
            )

            # phone is not a required field for customer_contact so update it if it only exists
            # customer serializer updated data
            if phone:
                related_customer.update(
                    phone=phone
                )
            if email:
                related_customer.update(
                    email=email
                )
            return JsonResponse(serializer.validated_data)
        return JsonResponse({"detail": "Invalid user selection"}, status=403)


class LogViewSet(GenericViewSet,
                 CreateModelMixin,
                 RetrieveModelMixin,
                 ListModelMixin,
                 UpdateModelMixin,
                 DestroyModelMixin):
    queryset = Log.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LogSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Log.objects.create(user=User.objects.get(id=serializer.validated_data['user_id']),
                           customer=Customer.objects.get(id=serializer.validated_data['customer_id']),
                           log=serializer.validated_data['log'])
        return JsonResponse(serializer.data)
