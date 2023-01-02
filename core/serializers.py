from dataclasses import fields
from rest_framework.serializers import ModelSerializer, SerializerMethodField

# Models
from .models import Entry, Event, Code

# Serializers
from account.serializers import AccountSerializer


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'amount')


class EntrySerializer(ModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'code', 'event', 'type', 'college', 'registered_by', 'name', 'phone', 'email',
                  'branch', 'class_name', 'payment_status', 'remark', 'mark_as_used')


class EntryDetailSerializer(ModelSerializer):
    event = SerializerMethodField()
    registered_by = SerializerMethodField()
    branch = SerializerMethodField()

    class Meta:
        model = Entry
        fields = ('id', 'code', 'event', 'type', 'college', 'registered_by', 'name', 'phone', 'email',
                  'branch', 'class_name', 'payment_status', 'remark', 'mark_as_used')

    def get_event(self, obj):
        return EventSerializer(obj.event).data

    def get_registered_by(self, obj):
        return AccountSerializer(obj.registered_by).data

    def get_branch(self, obj):
        return obj.get_branch_display()


class CodeSerializer(ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'


class CodeDetailSerializer(ModelSerializer):
    assigned_to = SerializerMethodField()
    created_on = SerializerMethodField()

    class Meta:
        model = Code
        fields = ('code', 'sub_code', 'assigned_to', 'is_active', 'created_on')

    def get_assigned_to(self, obj):
        return obj.assigned_to.name

    def get_created_on(self, obj):
        return obj.created_on.strftime("%c")
