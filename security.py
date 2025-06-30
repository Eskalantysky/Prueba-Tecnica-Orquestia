from fastapi import Header, HTTPException
from config import settings

def verificar_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="API Key inválida")

