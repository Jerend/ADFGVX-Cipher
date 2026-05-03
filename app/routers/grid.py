from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from app.cipher import ADFGVX_LETTERS
import json

router = APIRouter(prefix="/api/grid", tags=["grid"])

@router.post("/generate")
async def generate_grid(request: Request):
    """Генерирует новую таблицу шифра"""
    cipher = request.app.state.cipher
    grid = cipher.generate_grid()
    grid_json = {k: ''.join(v) for k, v in grid.items()}
    
    return {
        "status": "success",
        "message": "Grid generated and saved as current",
        "grid": grid_json,
        "adfgvx_letters": ADFGVX_LETTERS
    }

@router.post("/load")
async def load_grid(request: Request, file: UploadFile = File(...)):
    """Загружает таблицу шифра из JSON файла и сохраняет как текущую"""
    cipher = request.app.state.cipher
    
    try:
        content = await file.read()
        grid_data = json.loads(content)
        restored_grid = {}
        for k, v in grid_data.items():
            restored_grid[k] = (v[0], v[1])
        
        cipher.load_grid(restored_grid)
        
        return {
            "status": "success",
            "message": "Grid loaded and saved as current",
            "grid_size": len(restored_grid)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error loading grid: {str(e)}")

@router.get("/current")
async def get_current_grid(request: Request):
    """Возвращает текущую таблицу шифра"""
    cipher = request.app.state.cipher
    if not cipher.grid:
        return {
            "generated": False,
            "grid": None,
            "message": "No current grid available. Generate or load one first."
        }
    
    grid_json = {k: ''.join(v) for k, v in cipher.grid.items()}
    return {
        "generated": True,
        "grid": grid_json
    }

@router.get("/export")
async def export_grid(request: Request):
    """Экспортирует текущую таблицу шифра в JSON"""
    cipher = request.app.state.cipher
    if not cipher.grid:
        raise HTTPException(
            status_code=400, 
            detail="No grid to export. Generate or load one first."
        )
    
    grid_json = {k: ''.join(v) for k, v in cipher.grid.items()}
    return grid_json