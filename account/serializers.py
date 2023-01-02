from django.contrib.auth.password_validation import validate_password
from django.db import transaction

# RestFramework
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

# Models
from .models import Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'email', 'phone', 'year', 'password', 'branch',
                  'username', 'event_head', 'admin', 'desk')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        with transaction.atomic():
            # Account Information
            account = self.Meta.model(**validated_data)
            if password is not None:
                account.set_password(password)
            account.save()

        return account

    def validate(self, data):
        account = Account(**data)
        password = data.get('password')
        errors = dict()
        try:
            validate_password(password=password, user=account)
        except ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(AccountSerializer, self).validate(data)


class AccountListSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name')