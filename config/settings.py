"""Centralized configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

# Fixed base URLs
NVIDIA_NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"
XIAOMI_OPENAI_BASE_URL = "https://token-plan-sgp.xiaomimimo.com/v1"
XIAOMI_ANTHROPIC_BASE_URL = "https://token-plan-sgp.xiaomimimo.com/anthropic"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ==================== NVIDIA NIM Config ====================
    nvidia_nim_api_key: str = ""

    # ==================== Xiaomi Provider Config ====================
    xiaomi_api_key: str = ""
    xiaomi_protocol: str = "openai"  # "openai" or "anthropic"
    xiaomi_base_url: Optional[str] = None

    # ==================== Model ====================
    # All Claude model requests are mapped to this single model
    model: str = "moonshotai/kimi-k2-thinking"

    # ==================== Rate Limiting ====================
    nvidia_nim_rate_limit: int = 40
    nvidia_nim_rate_window: int = 60
    xiaomi_rate_limit: int = 40
    xiaomi_rate_window: int = 60

    # ==================== Fast Prefix Detection ====================
    fast_prefix_detection: bool = True

    # ==================== Logging ====================
    log_full_payloads: bool = False

    # ==================== Optimizations ====================
    enable_network_probe_mock: bool = True
    enable_title_generation_skip: bool = True

    # ==================== NIM Core Parameters ====================
    nvidia_nim_temperature: float = 1.0
    nvidia_nim_top_p: float = 1.0
    nvidia_nim_top_k: int = -1
    nvidia_nim_max_tokens: int = 81920
    nvidia_nim_presence_penalty: float = 0.0
    nvidia_nim_frequency_penalty: float = 0.0

    # ==================== NIM Advanced Parameters ====================
    nvidia_nim_min_p: float = 0.0
    nvidia_nim_repetition_penalty: float = 1.0
    nvidia_nim_seed: Optional[int] = None
    nvidia_nim_stop: Optional[str] = None

    # ==================== NIM Flag Parameters ====================
    nvidia_nim_parallel_tool_calls: bool = True
    nvidia_nim_return_tokens_as_token_ids: bool = False
    nvidia_nim_include_stop_str_in_output: bool = False
    nvidia_nim_ignore_eos: bool = False

    nvidia_nim_min_tokens: int = 0
    nvidia_nim_chat_template: str = ""
    nvidia_nim_request_id: str = ""

    # ==================== Thinking/Reasoning Parameters ====================
    nvidia_nim_reasoning_effort: str = "high"
    nvidia_nim_include_reasoning: bool = True

    # ==================== Xiaomi Core Parameters ====================
    xiaomi_temperature: float = 1.0
    xiaomi_top_p: float = 1.0
    xiaomi_top_k: int = -1
    xiaomi_max_tokens: int = 81920
    xiaomi_presence_penalty: float = 0.0
    xiaomi_frequency_penalty: float = 0.0

    # ==================== Xiaomi Advanced Parameters ====================
    xiaomi_min_p: float = 0.0
    xiaomi_repetition_penalty: float = 1.0
    xiaomi_seed: Optional[int] = None
    xiaomi_stop: Optional[str] = None

    # ==================== Xiaomi Flag Parameters ====================
    xiaomi_parallel_tool_calls: bool = True
    xiaomi_return_tokens_as_token_ids: bool = False
    xiaomi_include_stop_str_in_output: bool = False
    xiaomi_ignore_eos: bool = False

    xiaomi_min_tokens: int = 0
    xiaomi_chat_template: str = ""
    xiaomi_request_id: str = ""

    # ==================== Xiaomi Thinking/Reasoning Parameters ====================
    xiaomi_reasoning_effort: str = "high"
    xiaomi_include_reasoning: bool = True

    # ==================== Bot Wrapper Config ====================
    telegram_bot_token: Optional[str] = None
    telegram_api_id: Optional[str] = None  # Deprecated
    telegram_api_hash: Optional[str] = None  # Deprecated
    allowed_telegram_user_id: Optional[str] = None
    claude_workspace: str = "./agent_workspace"
    allowed_dir: str = ""
    max_cli_sessions: int = 10

    # ==================== Server ====================
    host: str = "0.0.0.0"
    port: int = 8082

    # Handle empty strings for optional int fields
    @field_validator("nvidia_nim_seed", "xiaomi_seed", mode="before")
    @classmethod
    def parse_optional_int(cls, v):
        if v == "" or v is None:
            return None
        return int(v)

    # Handle empty strings for optional string fields
    @field_validator(
        "nvidia_nim_stop",
        "xiaomi_stop",
        "telegram_bot_token",
        "telegram_api_id",
        "telegram_api_hash",
        "allowed_telegram_user_id",
        "xiaomi_base_url",
        mode="before",
    )
    @classmethod
    def parse_optional_str(cls, v):
        if v == "":
            return None
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
