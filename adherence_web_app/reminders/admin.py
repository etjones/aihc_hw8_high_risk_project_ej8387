from django.contrib import admin
from .models import AccountHolder, ServiceUser, MedicationRegime, Prescription, ServiceSession


@admin.register(AccountHolder)
class AccountHolderAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "sms_number", "user")
    search_fields = ("name", "email", "sms_number")


@admin.register(ServiceUser)
class ServiceUserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "sms_number", "account_holder")
    search_fields = ("name", "email", "sms_number")
    list_filter = ("account_holder",)


@admin.register(MedicationRegime)
class MedicationRegimeAdmin(admin.ModelAdmin):
    list_display = ("id", "service_user")
    list_filter = ("service_user",)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("medication", "dosage", "frequency", "start_date", "prescriber", "medication_regime")
    list_filter = ("medication_regime", "prescriber")
    search_fields = ("medication", "prescriber")


@admin.register(ServiceSession)
class ServiceSessionAdmin(admin.ModelAdmin):
    list_display = ("service_user", "medium", "start_time", "end_time")
    list_filter = ("medium", "service_user")
    search_fields = ("transcript", "outcome_notes")

# Register your models here.
