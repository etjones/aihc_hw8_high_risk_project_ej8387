from django.db import models
from django.contrib.auth.models import User
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import CircleMember, MedicationRegime, Prescription, ServiceSession


class AccountHolder(models.Model):
    name: models.CharField = models.CharField(max_length=255)
    email: models.EmailField = models.EmailField(unique=True)
    sms_number: models.CharField = models.CharField(max_length=32, blank=True)
    user: models.OneToOneField = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="account_holder"
    )

    def __str__(self) -> str:
        return self.name


class CircleMember(models.Model):
    name: models.CharField = models.CharField(max_length=255)
    email: models.EmailField = models.EmailField(blank=True)
    sms_number: models.CharField = models.CharField(max_length=32, blank=True)
    account_holder: models.ForeignKey = models.ForeignKey(
        AccountHolder, on_delete=models.CASCADE, related_name="circle_members"
    )
    prescriptions_description: models.TextField = models.TextField(
        blank=True, default=""
    )

    def __str__(self) -> str:
        return self.name

    def calculate_medication_times(
        self, day: datetime.date
    ) -> dict[datetime.datetime, "Prescription"]:
        """
        Return a dict mapping datetime (when medication is due) to the Prescription for this day.
        Only includes prescriptions that are active on the given day.
        """
        times: dict[datetime.datetime, "Prescription"] = {}
        for prescription in self.prescriptions.all():
            # Only include if prescription is active for this day
            if prescription.start_date and prescription.start_date > day:
                continue
            # Optionally handle end_date if you add it
            # Parse time_of_day if present
            if prescription.time_of_day:
                try:
                    # Try HH:MM format
                    hour, minute = map(int, prescription.time_of_day.split(":"))
                    dt = datetime.datetime.combine(day, datetime.time(hour, minute))
                except Exception:
                    # Fallback: treat as 'morning', 'evening', etc. (could be mapped)
                    dt = datetime.datetime.combine(
                        day, datetime.time(8, 0)
                    )  # default 8am
                times[dt] = prescription
        return times

    def calculate_next_contact_time(
        self,
    ) -> tuple[datetime.datetime | None, dict[datetime.datetime, "Prescription"]]:
        """
        Return the next contact time (datetime) and the dict of due medications for that time.
        """
        today = datetime.date.today()
        times = self.calculate_medication_times(today)
        if not times:
            return None, {}
        next_time = min(times.keys())
        return next_time, {next_time: times[next_time]}


class MedicationRegime(models.Model):
    circle_member: models.ForeignKey = models.ForeignKey(
        CircleMember, on_delete=models.CASCADE, related_name="medication_regimes"
    )
    natural_language_description: models.TextField = models.TextField(
        blank=True, default=""
    )
    # prescriptions: related_name from Prescription

    def __str__(self) -> str:
        return f"MedicationRegime for {self.circle_member.name} (ID: {self.id})"


class Prescription(models.Model):
    medication: models.CharField = models.CharField(max_length=255)
    dosage: models.CharField = models.CharField(max_length=128)
    frequency: models.CharField = models.CharField(max_length=128)
    start_date: models.DateField = models.DateField(blank=True, null=True)
    prescriber: models.CharField = models.CharField(max_length=255, blank=True)
    time_of_day: models.CharField = models.CharField(
        max_length=32,
        blank=True,
        help_text="Optional time of day for taking medication, e.g., '08:00' or 'morning'.",
    )
    circle_member: models.ForeignKey = models.ForeignKey(
        CircleMember, on_delete=models.CASCADE, related_name="prescriptions"
    )

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

    circle_member: models.ForeignKey = models.ForeignKey(
        CircleMember, on_delete=models.CASCADE, related_name="sessions"
    )
    medium: models.CharField = models.CharField(max_length=16, choices=MEDIUM_CHOICES)
    start_time: models.DateTimeField = models.DateTimeField()
    end_time: models.DateTimeField = models.DateTimeField(null=True, blank=True)
    transcript: models.TextField = models.TextField(blank=True)
    media_record: models.FileField = models.FileField(
        upload_to="session_media/", blank=True, null=True
    )
    outcome_notes: models.TextField = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Session for {self.circle_member.name} on {self.start_time:%Y-%m-%d %H:%M} ({self.medium})"
