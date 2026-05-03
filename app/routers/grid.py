from fastapi import APIRouter, HTTPException, Request
from app.cipher import ADFGVX_LETTERS

router = APIRouter(prefix="/api/grid", tags=["grid"])

@router.post("/generate")
async def generate_grid(request: Request):
    """Генерирует новую таблицу шифра"""
    cipher = request.app.state.cipher
    grid = cipher.generate_grid()
    grid_json = {k: ''.join(v) for k, v in grid.items()}
    
    return {
        "grid": grid_json,
        "adfgvx_letters": ADFGVX_LETTERS
    }

@router.get("/current")
async def get_current_grid(request: Request):
    """Возвращает текущую таблицу шифра"""
    cipher = request.app.state.cipher
    if not cipher.grid:
        return {"grid": None}
    
    grid_json = {k: ''.join(v) for k, v in cipher.grid.items()}
    return {"grid": grid_json}

@router.get("/export")
async def export_grid(request: Request):
    """Экспортирует текущую таблицу шифра в JSON"""
    cipher = request.app.state.cipher
    if not cipher.grid:
        raise HTTPException(status_code=400, detail="No grid to export")
    
    grid_json = {k: ''.join(v) for k, v in cipher.grid.items()}
    return grid_json