import json

from Iris_cli.auth import _update_config_for_provider, get_active_provider
from Iris_cli.config import load_config, save_config
from Iris_cli.setup import setup_model_provider


def _clear_provider_env(monkeypatch):
    for key in (
        "Metaxis_API_KEY",
        "OPENROUTER_API_KEY",
        "OPENAI_BASE_URL",
        "OPENAI_API_KEY",
        "LLM_MODEL",
    ):
        monkeypatch.delenv(key, raising=False)



def test_Metaxis_oauth_setup_keeps_current_model_when_syncing_disk_provider(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("Iris_HOME", str(tmp_path))
    _clear_provider_env(monkeypatch)

    config = load_config()

    prompt_choices = iter([0, 2])
    monkeypatch.setattr(
        "Iris_cli.setup.prompt_choice",
        lambda *args, **kwargs: next(prompt_choices),
    )
    monkeypatch.setattr("Iris_cli.setup.prompt", lambda *args, **kwargs: "")

    def _fake_login_Metaxis(*args, **kwargs):
        auth_path = tmp_path / "auth.json"
        auth_path.write_text(json.dumps({"active_provider": "Metaxis", "providers": {}}))
        _update_config_for_provider("Metaxis", "https://inference.example.com/v1")

    monkeypatch.setattr("Iris_cli.auth._login_Metaxis", _fake_login_Metaxis)
    monkeypatch.setattr(
        "Iris_cli.auth.resolve_Metaxis_runtime_credentials",
        lambda *args, **kwargs: {
            "base_url": "https://inference.example.com/v1",
            "api_key": "Metaxis-key",
        },
    )
    monkeypatch.setattr(
        "Iris_cli.auth.fetch_Metaxis_models",
        lambda *args, **kwargs: ["gemini-3-flash"],
    )

    setup_model_provider(config)
    save_config(config)

    reloaded = load_config()

    assert isinstance(reloaded["model"], dict)
    assert reloaded["model"]["provider"] == "Metaxis"
    assert reloaded["model"]["base_url"] == "https://inference.example.com/v1"
    assert reloaded["model"]["default"] == "anthropic/claude-opus-4.6"


def test_custom_setup_clears_active_oauth_provider(tmp_path, monkeypatch):
    monkeypatch.setenv("Iris_HOME", str(tmp_path))
    _clear_provider_env(monkeypatch)

    auth_path = tmp_path / "auth.json"
    auth_path.write_text(json.dumps({"active_provider": "Metaxis", "providers": {}}))

    config = load_config()

    monkeypatch.setattr("Iris_cli.setup.prompt_choice", lambda *args, **kwargs: 3)

    prompt_values = iter(
        [
            "https://custom.example/v1",
            "custom-api-key",
            "custom/model",
            "",
        ]
    )
    monkeypatch.setattr(
        "Iris_cli.setup.prompt",
        lambda *args, **kwargs: next(prompt_values),
    )

    setup_model_provider(config)
    save_config(config)

    reloaded = load_config()

    assert get_active_provider() is None
    assert isinstance(reloaded["model"], dict)
    assert reloaded["model"]["provider"] == "custom"
    assert reloaded["model"]["base_url"] == "https://custom.example/v1"
    assert reloaded["model"]["default"] == "custom/model"
