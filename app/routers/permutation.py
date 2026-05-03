from fastapi import APIRouter, HTTPException, Form, Request, UploadFile, File
import json

router = APIRouter(prefix="/api/permutation", tags=["permutation"])

@router.post("/generate")
async def generate_permutation(
    request: Request,
    keyword: str = Form(...)
):
    """Генерирует таблицу перестановки и сохраняет как текущую"""
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")
    
    cipher = request.app.state.cipher
    perm_table = cipher.generate_permutation_table(keyword)
    
    return {
        "status": "success",
        "message": "Permutation table generated and saved as current",
        "data": perm_table
    }

@router.post("/load")
async def load_permutation(request: Request, file: UploadFile = File(...)):
    """Загружает таблицу перестановки из JSON файла и сохраняет как текущую"""
    cipher = request.app.state.cipher
    
    try:
        content = await file.read()
        perm_data = json.loads(content)
        
        keyword = perm_data.get('keyword')
        if not keyword:
            raise ValueError("Keyword not found in permutation file")
        
        cipher.generate_permutation_table(keyword)
        
        return {
            "status": "success",
            "message": "Permutation table loaded and saved as current",
            "keyword": keyword
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error loading permutation: {str(e)}")

@router.get("/current")
async def get_current_permutation(request: Request):
    """Возвращает текущую таблицу перестановки"""
    cipher = request.app.state.cipher
    if not cipher.keyword:
        return {
            "generated": False,
            "permutation": None,
            "message": "No current permutation available. Generate or load one first."
        }
    
    perm_table = cipher.generate_permutation_table(cipher.keyword)
    return {
        "generated": True,
        "permutation": perm_table
    }

@router.get("/export")
async def export_permutation(request: Request):
    """Экспортирует текущую таблицу перестановки в JSON"""
    cipher = request.app.state.cipher
    if not cipher.keyword:
        raise HTTPException(
            status_code=400, 
            detail="No permutation to export. Generate or load one first."
        )
    
    perm_table = cipher.generate_permutation_table(cipher.keyword)
    return perm_table