from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, PhoneEntry, SpamReport, ContactList

class MyUserAdmin(UserAdmin):
    list_display = ('mobile', 'email', 'full_name',)
    search_fields = ('mobile', 'email', 'full_name')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('mobile',)

class SpamReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_entry', 'created_at')
    search_fields = ('user__mobile', 'phone_entry__number')
    list_filter = ('created_at',)

class PhoneEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'spam_score', 'is_spam')
    search_fields = ('name', 'number')
    list_filter = ('is_spam',)

class ContactListAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_name', 'contact_number')
    search_fields = ('user__mobile', 'contact_name', 'contact_number')
    list_filter = ('user',)

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(PhoneEntry, PhoneEntryAdmin)
admin.site.register(SpamReport, SpamReportAdmin)
admin.site.register(ContactList, ContactListAdmin)
