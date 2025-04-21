from django.db import models
from django.contrib.auth.models import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import ServiceUser, MedicationRegime, Prescription, ServiceSession

class AccountHolder(models.Model):
    name: models.CharField = models.CharField(max_length=255)
    email: models.EmailField = models.EmailField(unique=True)
    sms_number: models.CharField = models.CharField(max_length=32, blank=True)
    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_holder")

    def __str__(self) -> str:
        return self.name


class ServiceUser(models.Model):
    name: models.CharField = models.CharField(max_length=255)
    email: models.EmailField = models.EmailField(blank=True)
    sms_number: models.CharField = models.CharField(max_length=32, blank=True)
    account_holder: models.ForeignKey = models.ForeignKey(AccountHolder, on_delete=models.CASCADE, related_name="service_users")

    def __str__(self) -> str:
        return self.name


class MedicationRegime(models.Model):
    service_user: models.ForeignKey = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name="medication_regimes")
    # prescriptions: related_name from Prescription

    def __str__(self) -> str:
        return f"MedicationRegime for {self.service_user.name} (ID: {self.id})"


class Prescription(models.Model):
    medication: models.CharField = models.CharField(max_length=255)
    dosage: models.CharField = models.CharField(max_length=128)
    frequency: models.CharField = models.CharField(max_length=128)
    start_date: models.DateField = models.DateField()
    prescriber: models.CharField = models.CharField(max_length=255)
    medication_regime: models.ForeignKey = models.ForeignKey(MedicationRegime, on_delete=models.CASCADE, related_name="prescriptions")

    def __str__(self) -> str:
        return f"{self.medication} ({self.dosage})"


class ServiceSession(models.Model):
    MEDIUM_SMS = "sms"
    MEDIUM_VOICE = "voice_call"
    MEDIUM_EMAIL = "email"
    MEDIUM_CHOICES = [
        (MEDIUM_SMS, "SMS"),
        (MEDIUM_VOICE, "Voice Call"),
        (MEDIUM_EMAIL, "Email"),
    ]

    service_user: models.ForeignKey = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name="sessions")
    medium: models.CharField = models.CharField(max_length=16, choices=MEDIUM_CHOICES)
    start_time: models.DateTimeField = models.DateTimeField()
    end_time: models.DateTimeField = models.DateTimeField(null=True, blank=True)
    transcript: models.TextField = models.TextField(blank=True)
    media_record: models.FileField = models.FileField(upload_to="session_media/", blank=True, null=True)
    outcome_notes: models.TextField = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Session for {self.service_user.name} on {self.start_time:%Y-%m-%d %H:%M} ({self.medium})"
