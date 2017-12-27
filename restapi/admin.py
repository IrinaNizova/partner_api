from django.contrib import admin
from .models import *


class OfferingAdmin(admin.ModelAdmin):
    list_display = ('create_date', 'update_date', 'start_rotation_date', 'end_rotation_date',
                    'title', 'type', 'min_score', 'max_score', 'credit_organization')
    date_hierarchy = 'create_date'
    list_filter = ['update_date', 'start_rotation_date', 'type', 'credit_organization']
    search_fields = ('title', )
    ordering = ('min_score', 'max_score')


class CustomerProfileAdmin(admin.ModelAdmin):

    list_display = ('create_date', 'update_date', 'surname', 'first_name', 'middle_name',
                    'phone', 'passport_number', 'score')
    search_fields = ('surname', 'first_name', 'middle_name', 'phone', 'passport_number')
    list_filter = ['create_date', 'update_date']
    date_hierarchy = 'create_date'
    ordering = ('-create_date', 'score')


class RequestAdmin(admin.ModelAdmin):

    list_display = ('create_date',  'send_date', 'customer_profile', 'offering', 'status')
    search_fields = ('customer_profile', 'offering')
    list_filter = ['create_date', 'send_date']
    ordering = ('-create_date', 'status')
    date_hierarchy = 'create_date'


admin.site.register(CreditOrganization)
admin.site.register(Offering, OfferingAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(ReuqestToCredit, RequestAdmin)
