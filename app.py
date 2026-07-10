from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Crucial: Allows your HTML pages to talk to this server from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "booth_counts.json"
DEFAULT_DATA = {
    "Booth 1: Haunted House": 0,
    "Booth 2: Food Court": 0,
    "Booth 3: Arcade Games": 0,
    "Booth 4: Photobooth": 0
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

class TrafficUpdate(BaseModel):
    booth_id: str
    action: str

@app.get("/api/traffic")
def get_traffic():
    return load_data()

@app.post("/api/update")
def update_traffic(data: TrafficUpdate):
    current_data = load_data()
    if data.booth_id in current_data:
        if data.action == "check_in":
            current_data[data.booth_id] += 1
        elif data.action == "check_out" and current_data[data.booth_id] > 0:
            current_data[data.booth_id] -= 1
        
        save_data(current_data)
        return {"status": "success", "current_count": current_data[data.booth_id]}
    return {"status": "error", "message": "Booth not found"}