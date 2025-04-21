from django.contrib import admin
from .models import AccountHolder, CircleMember, MedicationRegime, Prescription, ServiceSession


@admin.register(AccountHolder)
class AccountHolderAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "sms_number", "user")
    search_fields = ("name", "email", "sms_number")


@admin.register(CircleMember)
class CircleMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "sms_number", "account_holder")
    search_fields = ("name", "email", "sms_number")
    list_filter = ("account_holder",)


@admin.register(MedicationRegime)
class MedicationRegimeAdmin(admin.ModelAdmin):
    list_display = ("id", "circle_member")
    list_filter = ("circle_member",)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("medication", "dosage", "frequency", "start_date", "prescriber", "circle_member")
    list_filter = ("circle_member", "prescriber")
    search_fields = ("medication", "prescriber")


@admin.register(ServiceSession)
class ServiceSessionAdmin(admin.ModelAdmin):
    list_display = ("circle_member", "medium", "start_time", "end_time")
    list_filter = ("medium", "circle_member")
    search_fields = ("transcript", "outcome_notes")

# Register your models here.
