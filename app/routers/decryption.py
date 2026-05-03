from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request
from typing import Optional
import json

router = APIRouter(prefix="/api/decrypt", tags=["decryption"])

@router.post("/")
async def decrypt(
    request: Request,
    ciphertext: Optional[str] = Form(None),
    cipher_file: Optional[UploadFile] = File(None),
    grid_file: UploadFile = File(...),
    permutation_file: UploadFile = File(...)
):
    """Дешифрует текст с использованием загруженных таблиц"""
    cipher = request.app.state.cipher
    
    try:
        # Загружаем таблицу шифра
        grid_content = await grid_file.read()
        grid_data = json.loads(grid_content)
        restored_grid = {}
        for k, v in grid_data.items():
            restored_grid[k] = (v[0], v[1])
        cipher.load_grid(restored_grid)
        
        # Загружаем таблицу перестановки
        perm_content = await permutation_file.read()
        perm_data = json.loads(perm_content)
        keyword = perm_data.get('keyword')
        if not keyword:
            raise ValueError("Keyword not found in permutation file")
        
        cipher.generate_permutation_table(keyword)
        
        # Получаем текст для дешифрования
        if ciphertext:
            text = ciphertext
        elif cipher_file:
            content = await cipher_file.read()
            text = content.decode('utf-8').strip()
        else:
            raise HTTPException(status_code=400, detail="Either ciphertext or cipher_file must be provided")
        
        decrypted = cipher.decrypt(text)
        
        return {
            "decrypted_text": decrypted,
            "stats": {
                "cipher_length": len(text),
                "decrypted_length": len(decrypted)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decryption error: {str(e)}")