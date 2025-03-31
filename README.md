# UT MSAI: AI In Healthcare: High Risk Project
# [Evan Jones](mailto:evan_jones@utexas.edu), `ej8387`, Spring 2025

Support code for the final "High Risk" project.

# Introduction and Motivation
Doctors prescribe a lot of medications, especially for very sick people. But very
sick and less capable people often have a hard time taking all their medications
at the right times reliable. Doctors call this "compliance", and it makes care 
much more difficult.

Various tools exist to help automate compliance with medical directives. But the 
most useful tool of all is people who care about a patient, helping them to take
their medications at the right times and dosages. Lacking that, can we use 
artificial intelligence, in the form of Large Language Models (LLMs) to deliver
some of the benefits that intervention from a concerned relation can offer?

Rather than trying to be an automated reminder service, this project attempts to
be an automated *relationship* service, with a component of health intervention
added alongside. At regular intervals, subscribers 

This project comprises:
- An automated conversation service that reaches out via text messages and/or voice messages.
- A conversation service to answer incoming messages or calls
- A web app that allows requesters to sign up for the service, set up care routines and medicine protocols, and check progress
- A database that encrypts and stores health data and conversation transcripts.

# Concerns
- Privacy & HIPAA obligations. 
- System misuse for non-medical purposes. If computers can form relationships with
  sick (and therefore often isolated and less competent) people, they can also 
  form extractive or abusive relationship.
