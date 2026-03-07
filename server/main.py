from fastapi import FastAPI
from server.websocket_handler import websocket_endpoint

app = FastAPI(title="AI Guidance Server MVP")

# Register the websocket endpoint
app.add_api_websocket_route("/ws", websocket_endpoint)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)