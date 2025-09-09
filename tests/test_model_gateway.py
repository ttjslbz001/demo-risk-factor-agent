from unittest import mock
import os
import types

import pytest

from src.gateway.model_gateway import (
    get_required_env,
    check_reachability,
    init_model,
    ModelGatewayError,
)


def test_get_required_env_reads_vars(monkeypatch):
    monkeypatch.setenv("TELENAV_API_KEY", "sk-abc")
    monkeypatch.setenv("TELENAV_BASE_URL", "https://example.test/v1/messages")
    monkeypatch.setenv("MODEL_NAME", "claude3.5-bedrock")
    cfg = get_required_env()
    assert cfg["api_key"] == "sk-abc"
    assert cfg["base_url"] == "https://example.test/v1/messages"
    assert cfg["model_name"] == "claude3.5-bedrock"


def test_get_required_env_raises_without_key(monkeypatch):
    monkeypatch.delenv("TELENAV_API_KEY", raising=False)
    with pytest.raises(ModelGatewayError):
        get_required_env()


def test_check_reachability_true(monkeypatch):
    monkeypatch.setenv("TELENAV_API_KEY", "sk-abc")
    monkeypatch.setenv("TELENAV_BASE_URL", "https://example.test/v1/messages")

    class DummyResp:
        status_code = 200

    dummy_requests = types.SimpleNamespace(options=lambda url, timeout=5.0: DummyResp())
    with mock.patch.dict("sys.modules", {"requests": dummy_requests}):
        assert check_reachability(0.1) is True


def test_check_reachability_false_on_exception(monkeypatch):
    monkeypatch.setenv("TELENAV_API_KEY", "sk-abc")
    monkeypatch.setenv("TELENAV_BASE_URL", "https://example.test/v1/messages")

    class DummyRequests:
        def options(self, *a, **k):  # type: ignore[no-untyped-def]
            raise RuntimeError("boom")

    with mock.patch.dict("sys.modules", {"requests": DummyRequests()}):
        assert check_reachability(0.1) is False


def test_init_model_raises_when_strands_missing(monkeypatch):
    monkeypatch.setenv("TELENAV_API_KEY", "sk-abc")
    monkeypatch.setenv("TELENAV_BASE_URL", "https://example.test/v1/messages")
    monkeypatch.setenv("MODEL_NAME", "claude3.5-bedrock")

    # Simulate ImportError by removing module from sys.modules and making import fail
    with mock.patch.dict("sys.modules", {"strands": None}, clear=False):
        with pytest.raises(ModelGatewayError):
            init_model()


