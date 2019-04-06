from django.contrib import admin
from .models import Fest, Event


@admin.register(Fest)
class FestAdmin(admin.ModelAdmin):
    list_display = ('organizer', 'name', 'website',
                    'start_date', 'end_date', 'manager_name')
    list_filter = ('events',)
    search_fields = ('name',)


admin.site.register(Event)
