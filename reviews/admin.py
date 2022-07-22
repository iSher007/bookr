from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *


class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ('title', 'publication_date', 'isbn', 'get_publisher')
    list_filter = ('publisher__name',)
    date_hierarchy = 'publication_date'
    search_fields = ('title', 'publisher__name',)

    @staticmethod
    def get_publisher(obj):
        return obj.publisher.name


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'email')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('initialled_name',)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Book, BookAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(BookContributor)
admin.site.register(Review)
admin.site.register(Session, SessionAdmin)
