"""LLM servisi — yapılandırma, durum sorgulama, bağlantı testi."""

from __future__ import annotations

from pathlib import Path

from bookmaker.llm.config import LLMConfig
from bookmaker.llm.openai import OpenAICompatibleClient


def get_status(project_root: str | Path) -> dict:
    """LLM durumunu döndürür."""
    cfg = LLMConfig(Path(project_root).resolve())
    if cfg.is_configured():
        return {"status": "Hazir", "provider": cfg.provider,
                "model": cfg.model, "configured": True}
    return {"status": "Yapilandirilmamis", "provider": "",
            "model": "deepseek-chat", "configured": False}


def configure(project_root: str | Path, provider: str,
              api_key: str, model: str) -> dict:
    """LLM yapılandırmasını kaydeder."""
    cfg = LLMConfig(Path(project_root).resolve())
    cfg.provider = provider
    cfg.api_key = api_key
    cfg.model = model
    return {"status": "ok", "provider": provider, "model": model}


def test_connection(project_root: str | Path) -> dict:
    """API bağlantısını test eder."""
    cfg = LLMConfig(Path(project_root).resolve())
    if not cfg.is_configured():
        return {"status": "error", "message": "LLM yapılandırılmamış"}
    try:
        client = OpenAICompatibleClient(
            api_key=cfg.api_key, model=cfg.model,
            base_url=cfg.base_url, timeout=30)
        result = client.test_connection()
        if result.get("status") == "ok":
            return {"status": "ok", "model": result.get("model", ""),
                    "message": "Bağlantı başarılı"}
        return {"status": "error", "message": result.get("error", "Bilinmeyen hata")}
    except Exception as e:
        return {"status": "error", "message": str(e)[:200]}
