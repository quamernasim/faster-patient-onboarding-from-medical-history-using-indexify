import base64
import io
import mimetypes
import os
from typing import Any, Dict, List, Optional, Union

from indexify_extractor_sdk import Content, Extractor, Feature
from openai import OpenAI
from pdf2image import convert_from_bytes
from pydantic import BaseModel, Field


class SchemaExtractorConfig(BaseModel):
    model: Optional[str] = Field(default="gpt-4o-2024-08-06")
    api_key: Optional[str] = Field(default=None)
    system_prompt: str = Field(default="Extract the information.")
    user_prompt: Optional[str] = Field(default=None)
    response_format: Optional[Dict[str, Any]] = Field(
        default={
            "properties": {"name": {"title": "Name", "type": "string"}},
            "required": ["name"],
            "title": "Event",
            "type": "object",
            "additionalProperties": False,
        }
    )


class SchemaExtractor(Extractor):
    name = "tensorlake/schema"
    description = "An extractor that let's you extract JSON from schemas."
    system_dependencies = []
    input_mime_types = [
        "text/plain",
    ]

    def __init__(self):
        super(SchemaExtractor, self).__init__()

    # def extract(
    #     self, content: Content, params: SchemaExtractorConfig
    # ) -> List[Union[Feature, Content]]:
    def extract(
        self
    ):
        json_schema = {
        'properties': {
            'name': {'title': 'Name', 'type': 'string'},
            'dob': {'title': 'Date of Birth', 'type': 'string'},
            'problem_description': {'title': 'Description of Problem or Complaints', 'type': 'string'},
            'accident_type': {'title': 'Is the present problem due to an injury?', 'type': 'string'},
            'accident_reported': {'title': 'Has the accident been reported?', 'type': 'string'},
            'family_history': {'title': 'Family History', 'type': 'string'},
            'job_description': {'title': 'Job Description', 'type': 'string'},
            'genral_symptoms': {'title': 'General Symptoms', 'type': 'string'},
            'muscles_and_joints_symptoms': {'title': 'Muscles and Joints Symptoms', 'type': 'string'},
            'cardiovascular_symptoms': {'title': 'Cardiovascular Symptoms', 'type': 'string'},
        },
        'required': ['name', 'dob', 'problem_description', 'accident_type', 'accident_reported', 'family_history', 'job_description', 'genral_symptoms', 'muscles_and_joints_symptoms', 'cardiovascular_symptoms'],
        'title': 'User',
        'type': 'object',
        "additionalProperties": False,
        }

        system_prompt = "Extract the medical history information from the document. You are only required give the information based on the given document. You are not allowed to add any additional information."
        params = SchemaExtractorConfig(
            model="gpt-4o-2024-08-06",
            system_prompt=system_prompt,
            # user_prompt=user_prompt,
            response_format=json_schema,  # Use the JSON schema here
        )

        content = Content.from_text("21/8/2024\nPersonal Medical History Template.\nDescription of problem or complaints:.\nDHBSFG DIKDAY\nhead ache\nBirth Date\nfever\n body pain\n10/8/2014\nvomiting\nHave you previously been treated for this.\ncondition? If yes, by whom?.\nno\nAre your present problems due to an injury? if.\nyes, please select from the list..\n Personal Injury\nIf this is an accident has it been reported? If\nyes, to whom?.\nAuto Carrier\nAre you now or have you ever been disabled?.\nNo\n! Jotform\nCreate your own automated PDFs with Jotform PDF Editor- It's free\nFamily History\nHabits\nDiabetes\nHeart Disease\nCoffee, # of cups per day.\n0\nFather\n Mother\nSmoking, # of packs per day.\nKidney Disease\n0.5\nMother\nAlcohol, # of drinks per week.\n0\nQuestions about Job.\nJob description:\nsoftwere developer\nHow many hours do you sit per day?\n8\nHow many hours do you stand per day?.\n2\nPlease mark if you ever had any of the following:.\nAppendicitis\nChicken Pox\n2\n! Jotform\nCreate your own automated PDFs with Jotform PDF Editor- It's free\nGeneral Symptoms\nMark the correct box for each symptom listed below:\n Allergy\nNever\nConvulsions\n Never\nDizziness\nNever\nFainting\nPreviously\nFatigue\nPreviously\nHeadache\nPreviously\n Nervousness\nPreviously\n Neuralgia\nNever\nNumbness\nNever\nPain in arms/legs/hands\n Previously\nHave you missed any work as a result of the accident? If so, how many days?\n3\n3\n! Jotform\nCreate your own automated PDFs with Jotform PDF Editor- It's free\nMuscles and Joints\nMark the correct box for each symptom listed below:\n Previously\nBackache\nFoot troublee\nPreviously\nHernia\nNever\nPain between shoulders\n Previously\nPainful tail bone.\n Never\nStiff neck\n Never\nSpinal curvature.\n Never\nSwollen joints.\nNever\nTremors\nNever\nTwitching\n Never\nWeakness\nPreviously\n4\n! Jotform\nCreate your own automated PDFs with Jotform PDF Editor- It's free\nCardiovascular\nMark the correct box for each symptom listed below:\nHigh blood pressure\nPreviously\nLow blood pressure\n Never\nPain over heart\n Never\nPoor circulation\nNever\nPrevious heart trouble\n Never\nStroke\n Never\nSwelling of ankles\n Never\nVaricose veins\nNever\nChest pain\nNever\nChronic cough\n Never\nDifficulty breathing\nNever\nOperations and Procedures\nVaccination\n2022\nAppendectomy\n2018\n5\n! Jotform\nCreate your own automated PDFs with Jotform PDF Editor- It's free\nGeneral\nHave you ever had Chiropractic care before?\nNo\nList any broken bones (fractures) or dislocation:\nleft arm broken\nHave you ever had any spinal taps/spinal injections?\nNo\nDo you suffer from any other condition other than for which you are now consulting us for?\nno\n6\n! Jotform\nCreate your own automated PDFs with Jotform PDF Editor- It's free\nConsent\nI hereby authorize the company to examine and treat my condition as deemed appropriate through the use\nof Chiropractic Care, and give authority for these procedures to be performed. It is understood and agreed\nthe amount paid to the Doctor for Xrays is for examination only and the Xray negatives will remain the\nproperty of this office, being on file where they may be seen at any time while a patient of the office. The\npatient also agrees that he/she is responsible for all bills incurred at this office. The Doctor will not be held\nresponsible for any pre-existing medically diagnosed conditions nor for any medical diagnosis\nSignature\nDate and Time\nWednesday, August 21, 2024 10:40\n7\n! Jotform\nCreate your own automated PDFs with Jotform PDF Editor- It's free")

        contents = []
        model_name = params.model
        key = params.api_key
        prompt = params.system_prompt
        query = params.user_prompt
        response_format = params.response_format



        text = content.data.decode("utf-8")
        if query is None:
            query = text
        response_content = self._process_text(
            model_name, key, prompt, query, response_format
        )

        contents.append(Content.from_text(response_content))
        return contents

    def _process_text(self, model_name, key, prompt, query, response_format):
        client = self._get_client(key)

        messages_content = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ]

        try:
            response = client.beta.chat.completions.parse(
                model=model_name,
                messages=messages_content,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "schema_response",  # Add a required name
                        "strict": True,
                        "schema": response_format,
                    },
                },
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Unable to process text: {str(e)}")
            raise e

    def _get_client(self, key):
        if ("OPENAI_API_KEY" not in os.environ) and (key is None):
            raise ValueError(
                "The OPENAI_API_KEY environment variable is not present and no API key was provided."
            )
        if ("OPENAI_API_KEY" in os.environ) and (key is None):
            return OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        return OpenAI(api_key=key)

    def sample_input(self) -> Content:
        return Content.from_text("Alice and Bob are going to a science fair on Friday.")


if __name__ == "__main__":

    
    extractor = SchemaExtractor()
    # results = extractor.extract(article, params=input_params)
    results = extractor.extract()
    print(results)