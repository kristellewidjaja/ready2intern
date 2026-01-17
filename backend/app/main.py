"""FastAPI main application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging

from app.api.routes import health, upload, companies, analyze, results

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Ready2Intern API",
    description="AI-powered resume evaluator for tech internships",
    version="1.0.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", '["http://localhost:5173"]')
# Parse JSON string to list
import json
origins = json.loads(cors_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(companies.router, prefix="/api", tags=["companies"])
app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(results.router, prefix="/api", tags=["results"])

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Ready2Intern API starting up...")
    logger.info(f"CORS enabled for origins: {origins}")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Ready2Intern API shutting down...")
