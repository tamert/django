from django.contrib import admin

from .models import Company, Post, Tag
from datetime import datetime
from django.contrib.admin import SimpleListFilter


class ActivationFilter(SimpleListFilter):
    title = 'activation'
    parameter_name = 'activation_code'

    def lookups(self, request, model_admin):
        return [('activated', 'Activated'), ('hold', 'On Hold')]

    def queryset(self, request, queryset):
        if self.value() == 'activated':
            return queryset.filter(activation_code__isnull=True)
        if self.value() == 'hold':
            return queryset.filter(activation_code__isnull=False)


def make_published(modeladmin, request, queryset):
    queryset.update(status=1, pub_date=datetime.now())


def make_unpublished(modeladmin, request, queryset):
    queryset.update(status=2, pub_date=None)


def make_disapproved(modeladmin, request, queryset):
    queryset.update(status=0, pub_date=None)


def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


def make_not_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)


make_unpublished.short_description = "Mark posts stories as unpublished"
make_published.short_description = "Mark posts stories as published"
make_disapproved.short_description = "Mark posts stories as disapproved"

make_featured.short_description = "Mark posts stories as featured"
make_not_featured.short_description = "Mark posts stories as featured"


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'position', 'is_featured', 'detail', 'location', 'status', 'pub_date')
    list_filter = (ActivationFilter, 'status', 'position')
    actions = [make_published, make_unpublished, make_disapproved, make_featured, make_not_featured]


admin.site.register(Company)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
