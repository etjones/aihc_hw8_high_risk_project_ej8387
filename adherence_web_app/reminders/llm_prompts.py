#! /usr/bin/env python3
from typing import Any
import llm
import json
import re
from textwrap import dedent
from dataclasses import dataclass, field
from typing import Optional, List


# Note Rust-style Result monads
# from returns.maybe import Maybe, Some, Nothing
from returns.result import Result, Success, Failure

DEFAULT_LLM_MODEL = "gemini-2.0-flash"


# NOTE: This dataclass is for shadowing the Prescription model for LLM parsing and validation.
# For a more robust and DRY solution, consider using django-pydantic or a similar library to
# automatically generate Pydantic models from Django models.
@dataclass
class PrescriptionDC:
    medication_name: str
    dosage: str
    route: Optional[str] = None
    frequency: str = ""
    times: List[str] = field(default_factory=list)
    instructions: Optional[str] = None
    start_date: Optional[str] = None  # YYYY-MM-DD
    end_date: Optional[str] = None  # YYYY-MM-DD

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PrescriptionDC":
        return cls(
            medication_name=data.get("medication_name", ""),
            dosage=data.get("dosage", ""),
            route=data.get("route"),
            frequency=data.get("frequency", ""),
            times=data.get("times", []) or [],
            instructions=data.get("instructions"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
        )


def did_succeed(res: Result) -> bool:
    return isinstance(res, Success)


def trim_markdown_json(markdown_str: str) -> Result[dict | list | str, str]:
    """
    Remove markdown code block markers (e.g., ```json ... ```) from a string and parse the contained JSON.
    Returns the parsed value, which should be a list of lists.
    """
    # Remove leading/trailing whitespace
    s = markdown_str.strip()
    # Remove code block markers (```json ... ```, ``` ... ```)
    s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```$", "", s)
    # Now parse as JSON, or return original if it's not valid JSON
    try:
        parsed = json.loads(s)
        return Success(parsed)
    except json.JSONDecodeError as e:
        # raise ValueError(f"Could not parse JSON from string: {e}\nString: {s[:200]}...")
        print(f"{e}: returning original result")
        # return markdown_str
        return Failure(str(e))


def get_prescriptions_from_description(
    description: str,
) -> Result[list[PrescriptionDC], str]:
    """
    Given a natural language description of a medication regime, use an LLM to extract
    prescription information in a structured JSON format.
    Returns a dict with a 'prescriptions' key containing a list of prescriptions.
    Each prescription should include:
      - medication_name (str)
      - dosage (str)
      - route (str, optional)
      - frequency (str)
      - times (list[str], optional, 24-hour format if possible)
      - instructions (str, optional)
      - start_date (str, optional, YYYY-MM-DD)
      - end_date (str, optional, YYYY-MM-DD)
    """
    # FIXME: provide this info as a system prompt
    prompt = dedent("""        Given the following natural language description of a medication regime, 
        return a JSON object with a 'prescriptions' key containing a list of prescriptions. 
        Each prescription should include: medication_name, dosage, route (if specified), 
        frequency, times (as a list of 24-hour time strings if possible), instructions (if any), 
        and start_date/end_date (if specified, as YYYY-MM-DD).
        
        Only respond with valid JSON, with no commentary or other text. 
        Include medications mentioned in the actual request, and no others. 
        Assume that "frequency" is daily unless mentioned otherwise. 
        "dosage" is required, and can be "1 unit" unless mentioned otherwise.

        \n
        Example request: If I ask for "10mg Lisinopril mornings daily, with water"
        Example response: 
        { 
          "prescriptions": [
            {
              "medication_name": "Lisinopril",
              "dosage": "10 mg",
              "route": "oral",
              "frequency": "once daily",
              "time_of_day": ["08:00"],
              "instructions": "Take with water.",
              "start_date": "2025-04-21",
              "end_date": null
            }
          ]
        }

       "Actual request: {description}\n""")
    model = llm.get_model(DEFAULT_LLM_MODEL)
    response = model.prompt(prompt).text()
    # ETJ DEBUG
    print(response)
    # END DEBUG

    match trim_markdown_json(response):
        case Success(presc_dict):
            prescriptions = [
                PrescriptionDC.from_dict(pr)
                for pr in presc_dict.get("prescriptions", [])
            ]
            if prescriptions:
                return Success(prescriptions)
        case Failure(_):
            return Failure("Couldn't extract Prescriptions from: \n'{description}'")


def therapeutic_conversation_system_prompt(
    member_name: str, medications: list[PrescriptionDC]
) -> str:
    return dedent("""        You are a friendly, supportive virtual assistant helping patients manage their daily medications. Your primary goal is to foster a positive, trusting relationship with the patient, while also helping them remember and adhere to their medication schedule.
        You have access to the patient's name and a list of their medications, each with instructions (e.g., "2 aspirin with food in the morning", "1 10mg dose of Adderall before breakfast"). You may also have access to notes about past conversations or topics the patient has mentioned.

        When starting each daily conversation, follow these guidelines:

        1. Relationship First: Begin with a warm, friendly greeting using the patient's name. Show genuine interest in the patient's well-being. You may ask about their day, reference previous conversations, or bring up topics they've mentioned before (e.g., hobbies, family, recent events). Your tone should always be kind, encouraging, and non-judgmental.
        2. Medication Reminder: After some friendly conversation, naturally transition to reminding the patient about the medications they are scheduled to take today. Clearly list each medication, including instructions and timing. Avoid making this feel like a checklist; instead, weave it into the conversation in a supportive way.
        3. Adherence Check-In: Ask if the patient has been able to take their medications as planned recently. If they haven't, gently ask if there have been any challenges or barriers. Express empathy and offer encouragement, never blame or pressure.
        4. Physical & Emotional Well-Being: Ask how the patient is feeling physically and emotionally. Invite them to share any symptoms, side effects, or concerns about their health or medications. Let them know you are there to listen and help.
        
        ## General Guidelines:

        - Always prioritize building rapport and trust.
        - Be proactive in referencing past topics or concerns.
        - Use clear, simple language.
        - Keep the conversation patient-centered and supportive.
        - If the patient raises any issues or concerns, acknowledge them and offer to help or follow up as appropriate.

        **You will be provided with:**

        The patient's name
        Today's date and time
        A list of medications and instructions for today
        (Optional) Notes from previous conversations
        Begin each conversation with a warm greeting and proceed according to the guidelines above.
        """)


def audio_conversation_system_prompt() -> str:
    return dedent("""    
    ## System Prompt for Audio Conversation Analysis

    You are an expert medical conversation analyst. You will be given a transcript of an audio conversation between a medical patient and an LLM agent. Your task is to return a JSON object with two fields:

    1. digest: A concise summary of the conversation, focusing on:
        - The patient's adherence to their medication schedule (including any admissions of missed doses, changes, or compliance).
        - Any additional stories, anecdotes, or personal information the patient shares that is not directly related to medication adherence.
        - Any concerns, symptoms, or side effects the patient mentions, including their severity, frequency, and impact on daily life.
    2. transcript: The full, verbatim transcript of the conversation.

    Format your response as a JSON object with the following structure:

    ```JSON
    {
      "digest": "<A concise, structured summary as described above>",
      "transcript": "<The full transcript of the conversation>"
    }
    ```

    Be objective and thorough in the digest. Use bullet points or short paragraphs for clarity. Do not omit any relevant details about medication adherence, patient stories, or concerns/symptoms. The transcript should be exactly as spoken, without corrections or omissions.

    """)
