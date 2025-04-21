This This document intends to layout the goals of the larger project so that we can develop fine-grained prompt instructions for each part of the project and use those to feed to an LLM such as claude sonnet 3.7

 the project should be broken up into a few different pieces first a Web App, which allows users to create a secure account to sign up a patient for regular contact from the project to specify medication, schedule and dosage routine that the project should check with the patient for and also track contacts with the patient and allow account deletion or data downloading.

 contacts with the patient and allow account deletion or data downloading.

Second is a regularly runnable application, which can contact a patient either via text message or via phone call if we can include voice to text interactions that should make contact with the patient on a regular schedule. Let's say daily start to create conversations keep transcripts of the conversations feed all past data to the LLM before talking so the alarm has memory of the relationship with a given patient andthe LLM should do. It's best to have in a real conversation with a patient. It's more important to develop a relationship and put the patient at ease and make them happy to talk with the service then it is to get right to business and remind them to take their medication. However, the final goal of the service is certainly to increase patient compliance with a medication regime and that needs to be a goal of the conversation.

. However, the final goal of the service is certainly to increase patient compliance with a medication regime and that needs to be a goal of the conversation.

Outstanding issues what's the best way to communicate via text message with client? How difficult is it to accept and create voice prompts talking on the telephone?

Outstanding issues what's the best way to communicate via text message with client? How difficult is it to accept and create voice prompts talking on the telephone?

How are we store? Patient data in a distributed system. There are some AWS services which may be suitable for this which aren't too expensive if we pay by usage it also may be usable simply to host this entire app from a local server for the duration of the project. That probably makes most sense for goals of this project.

. That probably makes most sense for goals of this project.

We also need to make sure that we're storing all data or sensitive all sensitive health, data and encrypted form and passwords has salted, etc. according to best security practices for storing information and databases.

We also need to make sure that we're storing all data or sensitive all sensitive health, data and encrypted form and passwords has salted, etc. according to best security practices for storing information and databases.

