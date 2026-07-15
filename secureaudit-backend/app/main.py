from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routers import auth, scans

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SecureAudit API",
    description="REST API for the SecureAudit web security audit platform ",
    version="1.0.0",
)


# CORS — enables the React front-end (localhost:5173) to communicate with the back-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the auth router # All routes in auth.py will be available
app.include_router(auth.router)
app.include_router(scans.router)


@app.get("/")
def root():
    return {"message": "SecureAudit API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}