#! /usr/bin/env python3
# from datetime import datetime
# from django.utils import timezone
from celery import shared_task
from .models import CircleMember


@shared_task
def send_daily_medication_reminders():
    """Run daily, gather next contact times and enqueue/send reminders for all CircleMembers."""
    # today = timezone.localdate()
    for member in CircleMember.objects.all():
        next_time, due = member.calculate_next_contact_time()
        if next_time:
            # TODO: Replace with actual REST call or queue logic
            print(
                f"Would send reminder for {member.name} at {next_time} for prescriptions: {list(due.values())}"
            )
