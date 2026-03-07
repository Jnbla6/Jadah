from pydantic import BaseModel
from typing import Optional

class AIPlanOutput(BaseModel):
    """
    This schema is strictly used to parse the JSON output that comes 
    directly from OpenAI before we send it to the client.
    """
    step: int
    instruction: str
    pointer_x: Optional[int]
    pointer_y: Optional[int]
    visual: str