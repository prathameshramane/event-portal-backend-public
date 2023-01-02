from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

# Views
from .views import AccountView, AccountRegisterView, AccountListView

urlpatterns = [
    path('', AccountView.as_view(), name="user-info"),
    path('register/', AccountRegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('account-list/', AccountListView.as_view(), name='account-list'),
]
