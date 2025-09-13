import secrets
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Dict, Any
import warnings
from datetime import timedelta

class Settings(BaseSettings):
    SECRET_KEY: str = Field("dev-secret-key", env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")

    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if len(v) < 32: 
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        if v == "dev-secret-key":
            Warning.warn("Using default SECRET_KEY in production is insecure!")
        return v
    
    @field_validator('ALGORITHM')
    @classmethod
    def validate_algorithm(cls, v: str) -> str:
        if v not in ['HS256', 'HS384', 'HS512']:
            raise ValueError(f"Attendance system only supports HMAC algorithms. Use HS256/384/512, not {v}")
        return v
    
    # jwt config
    WEB_SESSION_NO_EXPIRE: bool = Field(True, env="WEB_SESSION_NO_EXPIRE") # not expire session
    WEB_INACTIVITY_TIMEOUT_MINUTES: int = Field(60, env="WEB_INACTIVITY_TIMEOUT_MINUTES") # 1 hour inactivity timeout

    # Mobile settings - NO expiration
    MOBILE_SESSION_NO_EXPIRE: bool = Field(True, env="MOBILE_SESSION_NO_EXPIRE")  # Mobile never expires
    MOBILE_INACTIVITY_TIMEOUT_DAYS: int = Field(90, env="MOBILE_INACTIVITY_TIMEOUT_DAYS")  # 90 days inactivity
    # JWT Claims
    # Refresh token for additional security (optional)
    REFRESH_TOKEN_ENABLED: bool = Field(False, env="REFRESH_TOKEN_ENABLED")  # Not needed for mobile
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(365, env="REFRESH_TOKEN_EXPIRE_DAYS")  # 1 year if used

    JWT_ISSUER: str = Field("attendance-system-api", env="JWT_ISSUER")
    JWT_AUDIENCE: str = Field("attendance-web-mobile", env="JWT_AUDIENCE")

    # --- Mobile App Security ---
    MOBILE_APP_VERSION: str = Field("1.0.0", env="MOBILE_APP_VERSION")
    REQUIRE_DEVICE_ID: bool = Field(True, env="REQUIRE_DEVICE_ID")
    DEVICE_ID_SALT: str = Field(..., env="DEVICE_ID_SALT")  # For device fingerprinting
    
    # Biometric/Face ID settings
    ENABLE_BIOMETRIC_AUTH: bool = Field(True, env="ENABLE_BIOMETRIC_AUTH")
    BIOMETRIC_TIMEOUT_MINUTES: int = Field(5, env="BIOMETRIC_TIMEOUT_MINUTES")  # Re-auth with biometric after 5 min

    ALLOW_ORIGINS: List[str] = Field([
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000"
    ], env="ALLOW_ORIGINS")  # CORS

    # Auto token refresh settings
    AUTO_TOKEN_REFRESH_DAYS: int = Field(30, env="AUTO_TOKEN_REFRESH_DAYS")
    # --- Database ---
    DB_TYPE: str = Field("mysql", env="DB_CONNECTION")
    DB_USER: str = Field(..., env="DB_USERNAME")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(3306, env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_DATABASE")

    # Redis for device session management
    REDIS_URL: Optional[str] = Field(None, env="REDIS_URL")
    DEVICE_SESSION_TTL: int = Field(31536000, env="DEVICE_SESSION_TTL")  # 1 year in seconds

    @property
    def web_inactivity_timeout(self) -> timedelta:
        return timedelta(minutes=self.WEB_INACTIVITY_TIMEOUT_MINUTES)

    @property
    def mobile_inactivity_timeout(self) -> timedelta:
        return timedelta(days=self.MOBILE_INACTIVITY_TIMEOUT_DAYS)

    @property
    def biometric_timeout(self) -> timedelta:
        return timedelta(minutes=self.BIOMETRIC_TIMEOUT_MINUTES)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()