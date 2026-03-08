import asyncio
import json
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QCursor
import websockets
from client.screen_capture import capture_frame_base64
from shared.schemas import ClientMessage, ServerResponse

class WebSocketWorker(QThread):
    instruction_received = Signal(dict) # Passes the parsed instruction
    
    def __init__(self, uri: str):
        super().__init__()
        self.uri = uri
        self.task_text = ""
        self.running = False
        
    def set_task(self, task: str):
        self.task_text = task
        
    def stop(self):
        self.running = False
        self.wait()
        
    def run(self):
        self.running = True
        # Run the asyncio event loop inside this QThread
        asyncio.run(self.stream_loop())
        
    async def stream_loop(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                while self.running:
                    # 1. Capture screen
                    frame_b64 = capture_frame_base64()
                    
                    if not frame_b64:
                        await asyncio.sleep(1)
                        continue
                        
                    # 1.5 Get current mouse position
                    cursor_pos = QCursor.pos()
                    
                    # 2. Prepare payload
                    payload = ClientMessage(
                        image_base64=frame_b64,
                        task=self.task_text,
                        mouse_x=cursor_pos.x(),
                        mouse_y=cursor_pos.y()
                    )
                    
                    # 3. Send to server
                    await websocket.send(payload.json())
                    
                    # 4. Await response
                    response_str = await websocket.recv()
                    response_data = json.loads(response_str)
                    
                    # 5. Emit signal to update UI
                    if response_data.get("instruction"):
                        self.instruction_received.emit(response_data["instruction"])
                    
                    # MVP requirement: Capture every 1 second
                    await asyncio.sleep(1)
                    
        except Exception as e:
            print(f"WebSocket client error: {e}")