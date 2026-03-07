import json
from fastapi import WebSocket, WebSocketDisconnect
from shared.schemas import ClientMessage, ServerResponse
from server.vision_engine import process_frame
from server.ai_planner import get_next_step
from server.instruction_generator import generate_response

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 1. Receive data from client
            data = await websocket.receive_text()
            payload = ClientMessage.parse_raw(data)
            
            # 2. Vision Engine: Process frame and get elements
            elements = process_frame(payload.image_base64)
            
            # 3. AI Planner: Determine what to click based on task and screen elements
            ai_output = get_next_step(payload.task, elements)
            
            # 4. Instruction Generator: Format the response
            response = generate_response(ai_output)
            
            # 5. Send back to client
            await websocket.send_text(response.json())
            
    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"Error handling websocket: {e}")
        error_resp = ServerResponse(instruction=None, error=str(e))
        await websocket.send_text(error_resp.json())