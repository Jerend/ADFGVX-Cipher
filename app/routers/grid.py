from fastapi import APIRouter, HTTPException, Depends
from app.cipher import ADFGVXCipher, ADFGVX_LETTERS

router = APIRouter(prefix="/api/grid", tags=["grid"])

cipher_instance = None

def get_cipher():
    global cipher_instance
    if cipher_instance is None:
        cipher_instance = ADFGVXCipher()
    return cipher_instance

@router.post("/generate")
async def generate_grid(cipher: ADFGVXCipher = Depends(get_cipher)):
    """Генерирует новую таблицу шифра"""
    grid = cipher.generate_grid()
    grid_json = {k: ''.join(v) for k, v in grid.items()}
    
    return {
        "grid": grid_json,
        "adfgvx_letters": ADFGVX_LETTERS
    }

@router.get("/current")
async def get_current_grid(cipher: ADFGVXCipher = Depends(get_cipher)):
    """Возвращает текущую таблицу шифра"""
    if not cipher.grid:
        return {"grid": None}
    
    grid_json = {k: ''.join(v) for k, v in cipher.grid.items()}
    return {"grid": grid_json}

@router.get("/export")
async def export_grid(cipher: ADFGVXCipher = Depends(get_cipher)):
    """Экспортирует текущую таблицу шифра в JSON"""
    if not cipher.grid:
        raise HTTPException(status_code=400, detail="No grid to export")
    
    grid_json = {k: ''.join(v) for k, v in cipher.grid.items()}
    return grid_json