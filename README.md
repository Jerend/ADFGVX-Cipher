# ADFGVX-Cipher
Реализация шифра ADFGVX с REST API на FastAPI.

## Установка и запуск

```bash
# Создание виртуального окружения
python -m venv .venv

# Активация на Windows
.venv\\Scripts\\activate 

# Активация на Linux, Mac
source .venv/bin/activate 

# Установка зависимостей
pip install -r requirements.txt 

# Запуск сервера
python -m uvicorn app.main:app --reload
```
Документация API после запуска доступна по адресу: http://127.0.0.1:8000/docs