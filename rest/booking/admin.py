from django.contrib import admin
from .models import Table, Client, TypeTable


# Register your models here.
@admin.register(Table)
class PostAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'seats', 'booking_price', 'status_booking', 'status_published')
    # list_filter = ('status', 'created', 'publish', 'author')
    # search_fields = ('title', 'body')
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    # date_hierarchy = 'publish'
    # ordering = ('status', 'publish')


admin.site.register(Client)
admin.site.register(TypeTable)
