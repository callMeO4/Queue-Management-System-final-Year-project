from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Customer,
    Notification,
    Queue_Assignment,
    Queue_Ticket,
    Service,
    Teller,
    Teller_Service,
    User,
    Wait_Prediction,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
  fieldsets = UserAdmin.fieldsets + (('Role Information', {'fields': ('role',)}),)
  add_fieldsets = UserAdmin.add_fieldsets + (
      ('Role Information', {'fields': ('role',)}),
  )
  list_display = ('username', 'email', 'role', 'is_staff')
  list_filter = ('role', 'is_staff')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ('user', 'phone_number', 'created_at')
  search_fields = ('user__username', 'phone_number')


@admin.register(Teller)
class TellerAdmin(admin.ModelAdmin):
  list_display = (
      'teller_number',
      'user',
      'is_available',
      'current_status_state',
  )
  list_filter = ('is_available',)
  search_fields = ('teller_number', 'user__username')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
  list_display = ('name', 'estimated_service_duration')
  search_fields = ('name',)


@admin.register(Teller_Service)
class TellerServiceAdmin(admin.ModelAdmin):
  list_display = ('teller', 'service')
  list_filter = ('service',)


@admin.register(Queue_Ticket)
class QueueTicketAdmin(admin.ModelAdmin):
  list_display = (
      'ticket_number',
      'customer',
      'service',
      'status',
      'registration_time',
  )
  list_filter = ('status', 'service')
  search_fields = ('ticket_number', 'customer__user__username')


@admin.register(Queue_Assignment)
class QueueAssignmentAdmin(admin.ModelAdmin):
  list_display = ('ticket', 'teller', 'assigned_at', 'is_active')
  list_filter = ('is_active',)


@admin.register(Wait_Prediction)
class WaitPredictionAdmin(admin.ModelAdmin):
  list_display = ('ticket', 'teller', 'predicted_wait_time', 'created_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
  list_display = ('customer', 'is_read', 'created_at')
  list_filter = ('is_read',)

