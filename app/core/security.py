from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from typing import Optional, Dict, Any
import hashlib
import hmac

class JWTManager:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def create_mobile_token(self, user_id: str, device_id: str, device_info: Dict[str, Any]) -> str:
        