# Multi-Stage LLM Prompt for Django Medication Reminder Web App

## Overview

You are to generate a Django web application (using a SQLite database) for managing medication reminder calls. The app should be stylish, clean, and uncluttered, with a modern color scheme. The core functionality is for an AccountHolder to schedule reminder calls for a ServiceUser regarding their MedicationRegimes, and to manage users, reminders, and session transcripts.

## Entities

- **AccountHolder**: schedules ServiceUsers to receive medication reminders.
  - Fields: name, email, sms_number, service_users, normal Django User account
- **ServiceUser**: receives calls about MedicationRegimes.
  - Fields: name, email, sms_number, account_holder, medication_regimes, sessions
- **MedicationRegime**: one or more prescriptions for a ServiceUser.
  - Fields: service_user, prescriptions
- **Prescription**: details of a medication.
  - Fields: medication, dosage, frequency, start_date, prescriber
- **ServiceSession**: one instance of a reminder.
  - Fields: medium (SMS, voice call, email), start_time, end_time, transcript, media_record, outcome_notes

You now have the background for the app. Please don't write any code yet. I'll
proceed with instructions stage by stage and we'll make sure each is working before moving on to the next


### Multi-Stage Prompt

Submit each stage as a separate prompt to the LLM, in order:

#### Stage 1: Project Initialization with uv

> Use the `uv` package manager to initialize a new Python project suitable for a Django web app. Add Django and any basic development dependencies (such as `django`, `tailwindcss`, `python-dotenv`, etc.) to the requirements. Create the initial directory structure for the project but do not generate any Django apps or code yet. Output the commands and files created, and ensure the project is ready for the next step. 

#### Stage 2: Models and Relationships

> Write Django model classes for the following entities, with all specified fields and relationships: AccountHolder, ServiceUser, MedicationRegime, Prescription, ServiceSession. Use Django best practices and include type annotations.

#### Stage 3: Admin and Authentication

> Add Django admin registration for all models. Implement user registration and authentication for AccountHolders (using Django’s built-in User model).

#### Stage 4: Views and CRUD

> Write Django views, forms, and templates for CRUD operations on ServiceUsers, MedicationRegimes, Prescriptions, and ServiceSessions. Ensure only AccountHolders can manage their ServiceUsers and related data.

#### Stage 5: UI and Styling

> Apply a stylish, modern, uncluttered UI with a pleasing color scheme using a CSS framework (e.g., Tailwind). Ensure all pages are responsive and visually appealing.

#### Stage 6: Additional Features

> Add views to display transcripts and details for each ServiceSession, including outcome notes and any media records. Ensure data integrity and user-friendly navigation.

#### Stage 7: Initiate scheduled ServiceSessions with TBD REST calls

> MedicationRegimes call for medicines to be taken at different time. Add a service that examines MedicationRegimes or their associated Prescriptions and makes still-undefined REST api calls to initiate ServiceSessions

