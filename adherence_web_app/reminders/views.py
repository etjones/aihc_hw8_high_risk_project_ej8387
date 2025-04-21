from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AccountHolderRegistrationForm, CircleMemberForm, PrescriptionForm
from .models import CircleMember, AccountHolder, Prescription
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user

from returns.result import Result, Success, Failure


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AccountHolderRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been created. You can now log in."
            )
            return redirect(reverse("login"))
    else:
        form = AccountHolderRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def home(request: HttpRequest) -> HttpResponse:
    user = get_user(request)
    if user.is_authenticated:
        return redirect("/reminders/dashboard/")
    return render(request, "home.html")


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    user = request.user
    try:
        account_holder = user.account_holder
    except AccountHolder.DoesNotExist:
        messages.error(request, "AccountHolder profile not found.")
        return redirect("/accounts/profile/")

    circle_members = CircleMember.objects.filter(account_holder=account_holder)
    selected_cm_id = request.GET.get("circle_member_id")
    selected_cm = None
    prescriptions = []
    prescriptions_description = ""
    cm_form = CircleMemberForm()
    prescription_form = None
    editing_prescription = None
    # If no selection, auto-select first member if available
    if not selected_cm_id and circle_members.exists():
        selected_cm_id = str(circle_members.first().pk)
    if selected_cm_id:
        try:
            selected_cm = circle_members.get(pk=selected_cm_id)
            prescriptions = selected_cm.prescriptions.all()
            prescriptions_description = selected_cm.prescriptions_description
            prescription_form = PrescriptionForm()
        except CircleMember.DoesNotExist:
            selected_cm = None
            prescriptions = []
            prescriptions_description = ""
    # Handle add prescription
    if request.method == "POST" and "add_prescription" in request.POST:
        prescription_form = PrescriptionForm(request.POST)
        if selected_cm and prescription_form.is_valid():
            prescription = prescription_form.save(commit=False)
            prescription.circle_member = selected_cm
            prescription.save()
            messages.success(request, "Prescription added.")
            return redirect(
                f"{reverse('reminders:dashboard')}?circle_member_id={selected_cm.id}"
            )
    # Handle edit prescription
    if request.method == "POST" and "edit_prescription_id" in request.POST:
        edit_id = request.POST.get("edit_prescription_id")
        try:
            editing_prescription = selected_cm.prescriptions.get(pk=edit_id)
        except (AttributeError, Prescription.DoesNotExist):
            editing_prescription = None
        if editing_prescription:
            prescription_form = PrescriptionForm(
                request.POST, instance=editing_prescription
            )
            if prescription_form.is_valid():
                prescription_form.save()
                messages.success(request, "Prescription updated.")
                return redirect(
                    f"{reverse('reminders:dashboard')}?circle_member_id={selected_cm.id}"
                )
    # Handle delete prescription
    if request.method == "POST" and "delete_prescription_id" in request.POST:
        delete_id = request.POST.get("delete_prescription_id")
        try:
            del_presc = selected_cm.prescriptions.get(pk=delete_id)
            del_presc.delete()
            messages.success(request, "Prescription deleted.")
            return redirect(
                f"{reverse('reminders:dashboard')}?circle_member_id={selected_cm.id}"
            )
        except (AttributeError, Prescription.DoesNotExist):
            messages.error(request, "Prescription not found.")
    # Handle prescriptions_description update
    if request.method == "POST" and "update_prescriptions_description" in request.POST:
        update_cm_id = request.POST.get("circle_member_id")
        description = request.POST.get("prescriptions_description", "")
        if update_cm_id:
            try:
                update_cm = circle_members.get(pk=update_cm_id)
                update_cm.prescriptions_description = description
                update_cm.save()
                # --- LLM Prescription Extraction ---
                from .llm_prompts import get_prescriptions_from_description

                # result = get_prescriptions_from_description(description)
                match get_prescriptions_from_description(description):
                    case Success(prescription_dcs):
                        # if result.is_success:
                        # Remove all existing prescriptions for this member
                        update_cm.prescriptions.all().delete()
                        for presc_dc in prescription_dcs:
                            # Map PrescriptionDC fields to Prescription model fields
                            Prescription.objects.create(
                                medication=presc_dc.medication_name,
                                dosage=presc_dc.dosage,
                                frequency=presc_dc.frequency,
                                start_date=presc_dc.start_date or None,
                                prescriber="",  # Not present in DC, can be extended
                                circle_member=update_cm,
                            )
                        messages.success(
                            request,
                            "Prescriptions extracted and updated from description.",
                        )
                    case Failure(_):
                        messages.warning(
                            request,
                            "Prescriptions description updated, but could not extract structured prescriptions.",
                        )
                return redirect(
                    f"{reverse('reminders:dashboard')}?circle_member_id={update_cm_id}"
                )
            except CircleMember.DoesNotExist:
                messages.error(request, "Circle Member not found for update.")

    # Handle CircleMember add
    if request.method == "POST" and "add_circle_member" in request.POST:
        cm_form = CircleMemberForm(request.POST)
        if cm_form.is_valid():
            circle_member = cm_form.save(commit=False)
            circle_member.account_holder = account_holder
            circle_member.save()
            messages.success(request, f"Circle Member '{circle_member.name}' added.")
            return redirect("reminders:dashboard")
    context = {
        "circle_members": circle_members,
        "form": cm_form,
        "selected_cm": selected_cm,
        "prescriptions": prescriptions,
        "prescriptions_description": prescriptions_description,
        "prescription_form": prescription_form,
        "editing_prescription": editing_prescription,
    }
    return render(request, "dashboard.html", context)


@login_required
def edit_circle_member(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user
    account_holder = user.account_holder
    circle_member = CircleMember.objects.filter(
        account_holder=account_holder, pk=pk
    ).first()
    if not circle_member:
        messages.error(request, "Circle Member not found.")
        return redirect("reminders:dashboard")
    if request.method == "POST":
        form = CircleMemberForm(request.POST, instance=circle_member)
        if form.is_valid():
            form.save()
            messages.success(request, f"Circle Member '{circle_member.name}' updated.")
            return redirect("reminders:dashboard")
    else:
        form = CircleMemberForm(instance=circle_member)
    return render(
        request,
        "edit_circle_member.html",
        {"form": form, "circle_member": circle_member},
    )


@login_required
def delete_circle_member(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user
    account_holder = user.account_holder
    circle_member = CircleMember.objects.filter(
        account_holder=account_holder, pk=pk
    ).first()
    if not circle_member:
        messages.error(request, "Circle Member not found.")
    else:
        circle_member.delete()
        messages.success(request, "Circle Member deleted.")
    return redirect("reminders:dashboard")


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "profile.html")


def add_prescription(request: HttpRequest, circle_member_id: int) -> HttpResponse:
    return HttpResponse("Add Prescription - stub")


def edit_prescription(request: HttpRequest, pk: int) -> HttpResponse:
    return HttpResponse("Edit Prescription - stub")


def delete_prescription(request: HttpRequest, pk: int) -> HttpResponse:
    return HttpResponse("Delete Prescription - stub")
