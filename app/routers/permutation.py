from fastapi import APIRouter, HTTPException, Form, Request

router = APIRouter(prefix="/api/permutation", tags=["permutation"])

@router.post("/generate")
async def generate_permutation(
    request: Request,
    keyword: str = Form(...)
):
    """Генерирует таблицу перестановки на основе ключевого слова"""
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")
    
    cipher = request.app.state.cipher
    perm_table = cipher.generate_permutation_table(keyword)
    return perm_table

@router.get("/current")
async def get_current_permutation(request: Request):
    """Возвращает текущую таблицу перестановки"""
    cipher = request.app.state.cipher
    if not cipher.keyword:
        return {"permutation": None}
    
    perm_table = cipher.generate_permutation_table(cipher.keyword)
    return perm_table

@router.get("/export")
async def export_permutation(request: Request):
    """Экспортирует текущую таблицу перестановки в JSON"""
    cipher = request.app.state.cipher
    if not cipher.keyword:
        raise HTTPException(status_code=400, detail="No permutation table to export")
    
    perm_table = cipher.generate_permutation_table(cipher.keyword)
    return perm_table