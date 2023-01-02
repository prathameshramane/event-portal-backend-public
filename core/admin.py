from django.contrib import admin

from .models import Entry, Event, Code

# Register your models here.
admin.site.register(Entry)
admin.site.register(Event)
admin.site.register(Code)
