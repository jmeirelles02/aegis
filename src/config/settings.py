from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="Aegis - Shadow Architect")
    app_env: str = Field(default="development")
    app_debug: bool = Field(default=False)
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    google_api_key: str = Field(..., description="Google Gemini API Key")
    gemini_model: str = Field(default="gemini-1.5-pro")

    llm_temperature: float = Field(default=0.3, ge=0.0, le=1.0)
    llm_max_tokens: int = Field(default=8192, ge=1024)

    @field_validator("app_env")
    @classmethod
    def validate_env(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"app_env deve ser um de: {allowed}")
        return v

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

def get_settings() -> Settings:
    return Settings()

settings = get_settings()