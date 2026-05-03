from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request
from typing import Optional
import json

router = APIRouter(prefix="/api/decrypt", tags=["decryption"])

@router.post("/")
async def decrypt(
    request: Request,
    ciphertext: Optional[str] = Form(None),
    cipher_file: Optional[UploadFile] = File(None),
    use_current_grid: bool = Form(True),
    use_current_permutation: bool = Form(True),
    grid_file: Optional[UploadFile] = File(None),
    permutation_file: Optional[UploadFile] = File(None)
):
    """
    Дешифрует текст из строки или файла.
    
    Параметры:
    - ciphertext: зашифрованный текст
    - cipher_file: файл с зашифрованным текстом
    - use_current_grid: использовать текущую таблицу шифра (если есть)
    - use_current_permutation: использовать текущую таблицу перестановки (если есть)
    - grid_file: загрузить новую таблицу шифра из JSON файла
    - permutation_file: загрузить новую таблицу перестановки из JSON файла
    """
    cipher = request.app.state.cipher
    
    # 1. Загрузка таблицы шифра
    if grid_file:
        try:
            grid_content = await grid_file.read()
            grid_data = json.loads(grid_content)
            restored_grid = {}
            for k, v in grid_data.items():
                restored_grid[k] = (v[0], v[1])
            cipher.load_grid(restored_grid)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error loading grid file: {str(e)}")
    elif use_current_grid:
        if not cipher.grid:
            raise HTTPException(
                status_code=400, 
                detail="No current grid available. Either generate grid first (POST /api/grid/generate) or upload a grid file."
            )
    else:
        raise HTTPException(
            status_code=400, 
            detail="Either set use_current_grid=true or upload a grid file."
        )
    
    # 2. Загрузка таблицы перестановки
    if permutation_file:
        try:
            perm_content = await permutation_file.read()
            perm_data = json.loads(perm_content)
            keyword = perm_data.get('keyword')
            if not keyword:
                raise ValueError("Keyword not found in permutation file")
            cipher.generate_permutation_table(keyword)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error loading permutation file: {str(e)}")
    elif use_current_permutation:
        if not cipher.keyword:
            raise HTTPException(
                status_code=400, 
                detail="No current permutation available. Either generate permutation first (POST /api/permutation/generate) or upload a permutation file."
            )
    else:
        raise HTTPException(
            status_code=400, 
            detail="Either set use_current_permutation=true or upload a permutation file."
        )
    
    # 3. Получаем текст для дешифрования
    if ciphertext:
        text = ciphertext
    elif cipher_file:
        content = await cipher_file.read()
        text = content.decode('utf-8').strip()
    else:
        raise HTTPException(
            status_code=400, 
            detail="Either ciphertext or cipher_file must be provided"
        )
    
    # 4. Дешифруем
    try:
        decrypted = cipher.decrypt(text)
        
        return {
            "decrypted_text": decrypted,
            "stats": {
                "cipher_length": len(text),
                "decrypted_length": len(decrypted),
                "grid_source": "uploaded" if grid_file else "current",
                "permutation_source": "uploaded" if permutation_file else "current"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decryption error: {str(e)}")