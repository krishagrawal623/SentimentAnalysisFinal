import os
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# -----------------------
# Base paths
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
FRONTEND_DIST = os.path.join(BASE_DIR, "..", "frontend", "dist")

MODEL_PATH = os.path.join(BASE_DIR, "sentiment_model.pkl")
VECT_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

# -----------------------
# Load ML model
# -----------------------
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECT_PATH, "rb") as f:
    vectorizer = pickle.load(f)

# -----------------------
# FastAPI app
# -----------------------
app = FastAPI()

# -----------------------
# CORS (safe even for single deploy)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Input schema
# -----------------------
class TextInput(BaseModel):
    text: str

# -----------------------
# Prediction endpoint
# -----------------------
@app.post("/predict")
def predict_sentiment(data: TextInput):
    features = vectorizer.transform([data.text])
    prediction = model.predict(features)[0]
    sentiment = "positive" if int(prediction) == 1 else "negative"
    return {"sentiment": sentiment}

# -----------------------
# Serve React static files
# -----------------------
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")),
    name="assets",
)

# Serve React app
@app.get("/")
def serve_react():
    return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
