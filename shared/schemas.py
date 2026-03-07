from pydantic import BaseModel
from typing import Optional, List

class Point(BaseModel):
    x: int
    y: int

class ScreenElement(BaseModel):
    text: str
    x: int
    y: int
    width: int
    height: int

class ClientMessage(BaseModel):
    image_base64: str
    task: str

class Instruction(BaseModel):
    step: int
    instruction: str
    pointer: Optional[Point]
    visual: str = "arrow"

class ServerResponse(BaseModel):
    instruction: Optional[Instruction]
    error: Optional[str] = None