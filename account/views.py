from django.shortcuts import get_object_or_404

# RestFramework
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView

# Serializers
from .serializers import AccountSerializer, AccountListSerializer

# Models
from .models import Account

# Permissions
from .permissions import AdminClearance

# Create your views here.


class AccountView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id = request.user.id
        account = get_object_or_404(Account, pk=id)
        serializer = AccountSerializer(account)
        return Response(serializer.data)


class AccountRegisterView(CreateAPIView):
    permission_classes = (AdminClearance, )
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountListView(ListAPIView):
    permission_classes = (AdminClearance, )
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer
