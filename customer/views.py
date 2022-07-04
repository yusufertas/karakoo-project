from django.http import JsonResponse
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, ListModelMixin, \
    CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from customer.models import User, Customer, Log
from customer.permissions import IsOwner
from customer.serializers import UserSerializer, CustomerSerializer, LogSerializer


class UserViewSet(GenericViewSet,
                  CreateModelMixin,
                  RetrieveModelMixin,
                  ListModelMixin,
                  UpdateModelMixin):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer


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
        obj = Customer.objects.create(**serializer.data)
        obj.user = request.user
        obj.save()
        return JsonResponse(serializer.data)

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
        if request.user.is_superuser:
            return Response(super().update(request).data)
        if request.user.id == int(kwargs['pk']):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return JsonResponse(serializer.data)
        return JsonResponse({'detail': 'You do not have the permission to perform this action'},
                            status=403)


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
