from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request
from typing import Optional

router = APIRouter(prefix="/api/encrypt", tags=["encryption"])

@router.post("/")
async def encrypt(
    request: Request,
    plaintext: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    use_generated_grid: bool = Form(True)
):
    """Шифрует текст из строки или файла"""
    cipher = request.app.state.cipher
    
    if not cipher.grid:
        if use_generated_grid:
            cipher.generate_grid()
        else:
            raise HTTPException(status_code=400, detail="No grid loaded. Generate or load grid first.")
    
    if not cipher.keyword:
        raise HTTPException(status_code=400, detail="No keyword set. Generate permutation table first.")
    
    if plaintext:
        text = plaintext
    elif file:
        content = await file.read()
        text = content.decode('utf-8')
    else:
        raise HTTPException(status_code=400, detail="Either plaintext or file must be provided")
    
    encrypted = cipher.encrypt(text)
    
    return {
        "encrypted_text": encrypted,
        "stats": {
            "original_length": len(text),
            "encrypted_length": len(encrypted)
        }
    }