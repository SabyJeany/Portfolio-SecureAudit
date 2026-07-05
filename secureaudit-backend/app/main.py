from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SecureAudit API", version="1.0.0")

# CORS — enables the React front-end (localhost:5173) to communicate with the back-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SecureAudit API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}