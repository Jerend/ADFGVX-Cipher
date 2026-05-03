from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.cipher import ADFGVXCipher

# Единый экземпляр шифра
cipher = ADFGVXCipher()

app = FastAPI(title="ADFGVX Cipher API", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры с передачей экземпляра шифра
from app.routers import encryption_router, decryption_router, grid_router, permutation_router

app.include_router(encryption_router)
app.include_router(decryption_router)
app.include_router(grid_router)
app.include_router(permutation_router)

# Сохраняем экземпляр в app.state для доступа из роутеров
app.state.cipher = cipher

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