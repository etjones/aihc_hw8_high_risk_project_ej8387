# Django web app to accept and manage subscriptions 
Please write me a Django web app with a SQLite database. 
The app should have a stylish and appealing color schme and clean, uncluttered design.
The purpose of this app is for one person, perhaps a family member, the AccountHolder to schedule reminder calls to remind another person, the ServiceUser, to take his or her medications on a certain schedule, a MedicationRegime. It should have capacity to sign up new users, and to create, edit, and delete MedicationRegime reminder calls, as well as to view the transcript of each session

I'll describe the fields of each of these objects below:
- AccountHolder - this person schedules a ServiceUser to receive calls about a MedicationRegime
  - name
  - email
  - sms_number
  - service_users
  - normal Django User account
  
- ServiceUser - this person receives calls about their MedicationRegimes. They may or may not ever interact with the web app
  - name
  - email
  - sms_number
  - account_holder
  - medication_regimes
  - sessions

- MedicationRegime - One or more medications prescribed to a ServiceUser
  - service_user
  - prescriptions

- Prescription
  - medication
  - dosage
  - frequency
  - start_date
  - prescriber

- ServiceSession - One instance of a 
  - medium (one of SMS, voice call, emai)
  - start_time
  - end_time
  - transcript
  - media_record (recording of any data created during the session)
  - outcome_notes (record of whether a ServiceUser took a medication, was upset, requested help, etc.)

