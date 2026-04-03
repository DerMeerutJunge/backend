import os
import json
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "data.json"

# Init DB
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"waitlist": [], "survey": []}, f)


def read_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)


def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.get("/")
def home():
    return {"status": "OK"}


@app.post("/waitlist")
async def waitlist(req: Request):
    body = await req.json()
    data = read_db()

    body["createdAt"] = datetime.utcnow().isoformat()
    data["waitlist"].append(body)

    write_db(data)
    return {"success": True}


@app.post("/survey")
async def survey(req: Request):
    body = await req.json()
    data = read_db()

    body["createdAt"] = datetime.utcnow().isoformat()
    data["survey"].append(body)

    write_db(data)
    return {"success": True}


@app.get("/admin/data")
def download_data(key: str):
    if key != os.environ.get("ADMIN_KEY"):
        raise HTTPException(status_code=403, detail="Unauthorized")

    return FileResponse(DB_FILE, filename="data.json")
