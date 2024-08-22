from indexify_extractor_sdk import Content, Extractor, Feature
from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union, Tuple
import json

class InputParams(BaseModel):
    a: int = 0
    b: str = ""


class MyExtractor(Extractor):
    name = "yourorgname/myextractor"
    description = "Description of the extractor goes here."
    system_dependencies = []
    input_mime_types = ["text/plain"]

    def __init__(self):
        super().__init__()

    def extract(self, content: Content, params: InputParams) -> List[Union[Feature, Content]]:
        return [
            Content.from_text(
                text="Hello World", features=[Feature.embedding(values=[1, 2, 3])]
            ),
            Content.from_text(
                text="Pipe Baz", features=[Feature.embedding(values=[1, 2, 3])]
            ),
            Content.from_text(
                text="Hello World",
                features=[Feature.metadata({"key": "value"})],
            ),
        ]

    def sample_input(self) -> Content:
        return Content.from_text(text="Hello World")