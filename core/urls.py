from django.urls import path, include

# Rest Framework
from rest_framework.routers import DefaultRouter

# Core Views
from .views import EntryView, EventsView, MarkEntryView, EntryListView, EntryCSVView, CodeViewSet, AccountActiveCode

code_router = DefaultRouter()
code_router.register('', CodeViewSet, basename='code-viewset')

urlpatterns = [
    path('entry/', EntryListView.as_view()),
    path('entry/register/', EntryView.as_view()),
    path('entry/<int:pk>/', MarkEntryView.as_view()),
    path('events/', EventsView.as_view()),
    path('logs/', EntryCSVView.as_view()),
    path('codes/', include(code_router.urls)),
    path('mycode/', AccountActiveCode.as_view())
]
