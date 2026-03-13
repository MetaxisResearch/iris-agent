"""Tests for Codex auth — tokens stored in Iris auth store (~/.Iris/auth.json)."""

import json
import time
import base64
from pathlib import Path

import pytest
import yaml

from Iris_cli.auth import (
    AuthError,
    DEFAULT_CODEX_BASE_URL,
    PROVIDER_REGISTRY,
    _read_codex_tokens,
    _save_codex_tokens,
    _import_codex_cli_tokens,
    get_codex_auth_status,
    get_provider_auth_state,
    resolve_codex_runtime_credentials,
    resolve_provider,
)


def _setup_Iris_auth(Iris_home: Path, *, access_token: str = "access", refresh_token: str = "refresh"):
    """Write Codex tokens into the Iris auth store."""
    Iris_home.mkdir(parents=True, exist_ok=True)
    auth_store = {
        "version": 1,
        "active_provider": "openai-codex",
        "providers": {
            "openai-codex": {
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                "last_refresh": "2026-02-26T00:00:00Z",
                "auth_mode": "chatgpt",
            },
        },
    }
    auth_file = Iris_home / "auth.json"
    auth_file.write_text(json.dumps(auth_store, indent=2))
    return auth_file


def _jwt_with_exp(exp_epoch: int) -> str:
    payload = {"exp": exp_epoch}
    encoded = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).rstrip(b"=").decode("utf-8")
    return f"h.{encoded}.s"


def test_read_codex_tokens_success(tmp_path, monkeypatch):
    Iris_home = tmp_path / "Iris"
    _setup_Iris_auth(Iris_home)
    monkeypatch.setenv("Iris_HOME", str(Iris_home))

    data = _read_codex_tokens()
    assert data["tokens"]["access_token"] == "access"
    assert data["tokens"]["refresh_token"] == "refresh"


def test_read_codex_tokens_missing(tmp_path, monkeypatch):
    Iris_home = tmp_path / "Iris"
    Iris_home.mkdir(parents=True, exist_ok=True)
    # Empty auth store
    (Iris_home / "auth.json").write_text(json.dumps({"version": 1, "providers": {}}))
    monkeypatch.setenv("Iris_HOME", str(Iris_home))

    with pytest.raises(AuthError) as exc:
        _read_codex_tokens()
    assert exc.value.code == "codex_auth_missing"


def test_resolve_codex_runtime_credentials_missing_access_token(tmp_path, monkeypatch):
    Iris_home = tmp_path / "Iris"
    _setup_Iris_auth(Iris_home, access_token="")
    monkeypatch.setenv("Iris_HOME", str(Iris_home))

    with pytest.raises(AuthError) as exc:
        resolve_codex_runtime_credentials()
    assert exc.value.code == "codex_auth_missing_access_token"
    assert exc.value.relogin_required is True


def test_resolve_codex_runtime_credentials_refreshes_expiring_token(tmp_path, monkeypatch):
    Iris_home = tmp_path / "Iris"
    expiring_token = _jwt_with_exp(int(time.time()) - 10)
    _setup_Iris_auth(Iris_home, access_token=expiring_token, refresh_token="refresh-old")
    monkeypatch.setenv("Iris_HOME", str(Iris_home))

    called = {"count": 0}

    def _fake_refresh(tokens, timeout_seconds):
        called["count"] += 1
        return {"access_token": "access-new", "refresh_token": "refresh-new"}

    monkeypatch.setattr("Iris_cli.auth._refresh_codex_auth_tokens", _fake_refresh)

    resolved = resolve_codex_runtime_credentials()

    assert called["count"] == 1
    assert resolved["api_key"] == "access-new"


def test_resolve_codex_runtime_credentials_force_refresh(tmp_path, monkeypatch):
    Iris_home = tmp_path / "Iris"
    _setup_Iris_auth(Iris_home, access_token="access-current", refresh_token="refresh-old")
    monkeypatch.setenv("Iris_HOME", str(Iris_home))

    called = {"count": 0}

    def _fake_refresh(tokens, timeout_seconds):
        called["count"] += 1
        return {"access_token": "access-forced", "refresh_token": "refresh-new"}

    monkeypatch.setattr("Iris_cli.auth._refresh_codex_auth_tokens", _fake_refresh)

    resolved = resolve_codex_runtime_credentials(force_refresh=True, refresh_if_expiring=False)

    assert called["count"] == 1
    assert resolved["api_key"] == "access-forced"


def test_resolve_provider_explicit_codex_does_not_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    assert resolve_provider("openai-codex") == "openai-codex"


def test_save_codex_tokens_roundtrip(tmp_path, monkeypatch):
    Iris_home = tmp_path / "Iris"
    Iris_home.mkdir(parents=True, exist_ok=True)
    (Iris_home / "auth.json").write_text(json.dumps({"version": 1, "providers": {}}))
    monkeypatch.setenv("Iris_HOME", str(Iris_home))

    _save_codex_tokens({"access_token": "at123", "refresh_token": "rt456"})
    data = _read_codex_tokens()

    assert data["tokens"]["access_token"] == "at123"
    assert data["tokens"]["refresh_token"] == "rt456"


def test_import_codex_cli_tokens(tmp_path, monkeypatch):
    codex_home = tmp_path / "codex-cli"
    codex_home.mkdir(parents=True, exist_ok=True)
    (codex_home / "auth.json").write_text(json.dumps({
        "tokens": {"access_token": "cli-at", "refresh_token": "cli-rt"},
    }))
    monkeypatch.setenv("CODEX_HOME", str(codex_home))

    tokens = _import_codex_cli_tokens()
    assert tokens is not None
    assert tokens["access_token"] == "cli-at"
    assert tokens["refresh_token"] == "cli-rt"


def test_import_codex_cli_tokens_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "nonexistent"))
    assert _import_codex_cli_tokens() is None


def test_codex_tokens_not_written_to_shared_file(tmp_path, monkeypatch):
    """Verify Iris never writes to ~/.codex/auth.json."""
    Iris_home = tmp_path / "Iris"
    codex_home = tmp_path / "codex-cli"
    Iris_home.mkdir(parents=True, exist_ok=True)
    codex_home.mkdir(parents=True, exist_ok=True)

    (Iris_home / "auth.json").write_text(json.dumps({"version": 1, "providers": {}}))
    monkeypatch.setenv("Iris_HOME", str(Iris_home))
    monkeypatch.setenv("CODEX_HOME", str(codex_home))

    _save_codex_tokens({"access_token": "Iris-at", "refresh_token": "Iris-rt"})

    # ~/.codex/auth.json should NOT exist
    assert not (codex_home / "auth.json").exists()

    # Iris auth store should have the tokens
    data = _read_codex_tokens()
    assert data["tokens"]["access_token"] == "Iris-at"


def test_resolve_returns_Iris_auth_store_source(tmp_path, monkeypatch):
    Iris_home = tmp_path / "Iris"
    _setup_Iris_auth(Iris_home)
    monkeypatch.setenv("Iris_HOME", str(Iris_home))

    creds = resolve_codex_runtime_credentials()
    assert creds["source"] == "Iris-auth-store"
    assert creds["provider"] == "openai-codex"
    assert creds["base_url"] == DEFAULT_CODEX_BASE_URL
