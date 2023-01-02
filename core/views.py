from django.http import Http404, HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404

# RestFramework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_406_NOT_ACCEPTABLE
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter

# Permissions
from account.permissions import DeskClearance, EventHeadClearance, AdminClearance

# Serializers
from .serializers import EntryDetailSerializer, EntrySerializer, EventSerializer, CodeSerializer, CodeDetailSerializer

# Utils
from .utils import send_register_success, check_if_exists
import csv

# Modes
from .models import Event, Entry, Code

# Create your views here.


class EntryView(APIView):
    permission_classes = (DeskClearance, )

    def post(self, request):
        data = request.data
        data['registered_by'] = request.user.id
        if(check_if_exists(data)):
            return Response(status=HTTP_406_NOT_ACCEPTABLE, data={'error': 'Max entries reached!'})
        try:
            main_code = data['main_code']
            code_obj = get_object_or_404(Code, code=main_code)
            email = data["email"]
            serializer = EntrySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            code_obj.sub_code = code_obj.sub_code + 1
            code_obj.save()
            entry = Entry.objects.get(code=data["code"])
            send_register_success(email=email, entry=entry)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class EntryListView(ListAPIView):
    permission_classes = (EventHeadClearance, )
    serializer_class = EntryDetailSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "code"]

    def get_queryset(self):
        account = self.request.user
        return Entry.objects.filter(event__event_head=account.id)


class MarkEntryView(APIView):
    permission_classes = (EventHeadClearance, )

    def get_object(self, pk):
        try:
            return Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        entry = self.get_object(pk)
        serializer = EntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventsView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EntryCSVView(APIView):
    permission_classes = (AdminClearance, )

    def get_content_list(self, event, branch, type):
        content = []
        if event and branch and type:
            query_set = Entry.objects.filter(
                event=event, branch=branch, type=type)
        elif event and branch:
            query_set = Entry.objects.filter(event=event, branch=branch)
        elif event and type:
            query_set = Entry.objects.filter(event=event, type=type)
        elif branch and type:
            query_set = Entry.objects.filter(branch=branch, type=type)
        elif event:
            query_set = Entry.objects.filter(event=event)
        elif branch:
            query_set = Entry.objects.filter(branch=branch)
        elif type:
            query_set = Entry.objects.filter(type=type)
        else:
            query_set = Entry.objects.all()

        for entry in query_set:
            content.append(
                [
                    timezone.localtime(entry.register_date).strftime(
                        '%d-%m-%Y %I:%M%p'),
                    entry.code,
                    entry.get_type_display(),
                    entry.college,
                    entry.registered_by.name,
                    entry.name, entry.phone,
                    entry.get_branch_display(),
                    entry.event.name,
                    entry.event.amount
                ])
        return content

    def get(self, request):
        event = self.request.query_params.get('event')
        branch = self.request.query_params.get('branch')
        type = self.request.query_params.get('type')

        response = HttpResponse(content_type='application/csv')
        writer = csv.writer(response)
        writer.writerow([
            'Date Registered',
            'Code',
            'Type',
            'College',
            'Registered By',
            'Participants Name',
            'Contact No',
            'Branch',
            'Event',
            'Amount'
        ])

        content = self.get_content_list(event=event, branch=branch, type=type)
        writer.writerows(content)

        filename = f'Log Sheet - {event}'
        if event:
            filename = filename + f' - {event}'
        if branch:
            filename = filename + f' - {branch}'
        if type:
            filename = filename + f' - {type}'

        filename = filename + '.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class CodeViewSet(ModelViewSet):
    permission_classes = (AdminClearance, )
    queryset = Code.objects.all()
    serializer_class = CodeSerializer

    def create(self, request, * args, **kwargs):
        Code.objects.filter(
            assigned_to=request.data['assigned_to']).update(is_active=False)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        codes_list = Code.objects.all()
        return Response(CodeDetailSerializer(codes_list, many=True).data)


class AccountActiveCode(APIView):
    permission_classes = (DeskClearance, )

    def get(self, request):
        code = get_object_or_404(
            Code, assigned_to=request.user, is_active=True)
        return Response(CodeSerializer(code).data)
