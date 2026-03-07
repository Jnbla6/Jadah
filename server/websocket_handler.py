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
            # 1. Receive data
            data = await websocket.receive_text()
            payload = ClientMessage.parse_raw(data)
            print("\n" + "="*40)
            print(f"🎯 New Task Received: '{payload.task}'")
            print("📸 1. Processing screenshot...")
            
            # 2. Vision Engine
            elements = process_frame(payload.image_base64)
            print(f"👀 2. Vision Engine found {len(elements)} text elements on your screen!")
            
           # 3. AI Planner
            print("🧠 3. Local AI is thinking... (Please wait, this can take 15-60 seconds!)")
            ai_output = get_next_step(payload.task, elements)
            
            # 4. Instruction Generator
            if ai_output and ai_output.pointer_x is not None:
                print(f"✅ 4. AI found the button! Drawing arrow at X:{ai_output.pointer_x}, Y:{ai_output.pointer_y}")
            else:
                print("⚠️ 4. AI got confused by too much text and couldn't find the coordinates!")
                
            response = generate_response(ai_output)
            
            # 5. Send back to client
            await websocket.send_text(response.json())
            print("="*40 + "\n")
            
    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"Error handling websocket: {e}")
        error_resp = ServerResponse(instruction=None, error=str(e))
        await websocket.send_text(error_resp.json())