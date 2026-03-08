import json
import math
from fastapi import WebSocket, WebSocketDisconnect
from shared.schemas import ClientMessage, ServerResponse, Instruction
from server.vision_engine import process_frame
from server.ai_planner import get_next_step
from server.instruction_generator import generate_response

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # State tracking for the current session
    active_target_x = None
    active_target_y = None
    
    try:
        while True:
            # 1. Receive data
            data = await websocket.receive_text()
            payload = ClientMessage.parse_raw(data)
            print("\n" + "="*40)
            print(f"🎯 New Task Received: '{payload.task}'")
            print("📸 1. Processing screenshot...")
            
            # Check mouse coordinates
            mouse_x = payload.mouse_x
            mouse_y = payload.mouse_y
            if mouse_x is not None and mouse_y is not None:
                print(f"🖱️ User mouse is at X:{mouse_x}, Y:{mouse_y}")
            
            # 2. Vision Engine
            elements = process_frame(payload.image_base64)
            print(f"👀 2. Vision Engine found {len(elements)} text elements on your screen!")
            
            # 3. AI Planner
            print("🧠 3. Local AI is thinking... (Please wait, this can take 15-60 seconds!)")
            ai_output = get_next_step(payload.task, elements)
            
            is_target_reached = False
            
            # 4. Instruction Generator
            if ai_output and ai_output.pointer_x is not None:
                print(f"✅ 4. AI found the button! Drawing arrow at X:{ai_output.pointer_x}, Y:{ai_output.pointer_y}")
                active_target_x = ai_output.pointer_x
                active_target_y = ai_output.pointer_y
                
                # Check proximity if mouse is being hovered
                if mouse_x is not None and mouse_y is not None:
                    distance = math.hypot(active_target_x - mouse_x, active_target_y - mouse_y)
                    print(f"📏 Distance to target: {distance:.2f}px")
                    if distance < 60:
                        is_target_reached = True
                        print("✨ Target reached! Moving onto next step (instruction update).")
            else:
                print("⚠️ 4. AI got confused by too much text and couldn't find the coordinates!")
                active_target_x = None
                active_target_y = None
                
            response = generate_response(ai_output)
            
            # Inject our is_target_reached state into the response if there's an instruction
            if response.instruction is not None:
                response.instruction.is_target_reached = is_target_reached
            
            # 5. Send back to client
            await websocket.send_text(response.json())
            print("="*40 + "\n")
            
    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error handling websocket: {e}")
        error_resp = ServerResponse(instruction=None, error=str(e))
        await websocket.send_text(error_resp.json())