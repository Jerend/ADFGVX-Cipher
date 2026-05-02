from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import encryption_router, decryption_router, grid_router, permutation_router

app = FastAPI(title="ADFGVX Cipher API", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(encryption_router)
app.include_router(decryption_router)
app.include_router(grid_router)
app.include_router(permutation_router)

@app.get("/")
async def root():
    return {
        "message": "ADFGVX Cipher API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}