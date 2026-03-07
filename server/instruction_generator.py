from shared.schemas import ServerResponse, Instruction, Point
from server.models import AIPlanOutput
from typing import Optional

def generate_response(ai_plan: Optional[AIPlanOutput]) -> ServerResponse:
    """Converts the internal AI output into the client-facing ServerResponse."""
    if not ai_plan:
        return ServerResponse(instruction=None, error="Failed to generate AI plan.")
        
    pointer = None
    if ai_plan.pointer_x is not None and ai_plan.pointer_y is not None:
        pointer = Point(x=ai_plan.pointer_x, y=ai_plan.pointer_y)
        
    instruction = Instruction(
        step=ai_plan.step,
        instruction=ai_plan.instruction,
        pointer=pointer,
        visual=ai_plan.visual
    )
    
    return ServerResponse(instruction=instruction, error=None)