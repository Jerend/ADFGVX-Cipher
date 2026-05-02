from fastapi import APIRouter, HTTPException, Depends, Form
from app.cipher import ADFGVXCipher

router = APIRouter(prefix="/api/permutation", tags=["permutation"])

cipher_instance = None

def get_cipher():
    global cipher_instance
    if cipher_instance is None:
        cipher_instance = ADFGVXCipher()
    return cipher_instance

@router.post("/generate")
async def generate_permutation(
    keyword: str = Form(...),
    cipher: ADFGVXCipher = Depends(get_cipher)
):
    """Генерирует таблицу перестановки на основе ключевого слова"""
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")
    
    perm_table = cipher.generate_permutation_table(keyword)
    return perm_table

@router.get("/current")
async def get_current_permutation(cipher: ADFGVXCipher = Depends(get_cipher)):
    """Возвращает текущую таблицу перестановки"""
    if not cipher.keyword:
        return {"permutation": None}
    
    perm_table = cipher.generate_permutation_table(cipher.keyword)
    return perm_table

@router.get("/export")
async def export_permutation(cipher: ADFGVXCipher = Depends(get_cipher)):
    """Экспортирует текущую таблицу перестановки в JSON"""
    if not cipher.keyword:
        raise HTTPException(status_code=400, detail="No permutation table to export")
    
    perm_table = cipher.generate_permutation_table(cipher.keyword)
    return perm_table