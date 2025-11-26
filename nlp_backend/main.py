from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nlp_backend.routers import translation

app = FastAPI(title="PictoLink NLP Backend")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://picto-link.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(translation.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    from nlp_backend.services.catalog import CatalogService
    import os
    
    # Path to data
    # Assuming run from root or nlp_backend dir, adjust as needed
    # We copied data to nlp_backend/data/arasaac_catalog.jsonl
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "arasaac_catalog.jsonl")
    
    service = CatalogService.get_instance()
    service.load_data(data_path)

@app.get("/health")
def health_check():
    return {"status": "ok"}
