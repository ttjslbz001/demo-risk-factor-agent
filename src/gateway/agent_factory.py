import os
from typing import Any, Dict


class ModelGatewayError(RuntimeError):
    pass


def get_required_env() -> Dict[str, str]:
    # Read from current process environment only; higher layers may load .env
    api_key = os.environ.get("TELENAV_API_KEY")
    base_url = os.environ.get(
        "TELENAV_BASE_URL", "https://us-ailab-api.telenav.com/v1/messages"
    )
    model_name = os.environ.get("MODEL_NAME", "claude3.5-bedrock")
    if not api_key:
        raise ModelGatewayError("TELENAV_API_KEY is not set")
    return {"api_key": api_key, "base_url": base_url, "model_name": model_name}


def init_agent() -> Any:
    """
    Initialize a strands Agent backed by OpenAIModel and expose a .complete-compatible adapter.
    """
    # Import strands components; allow tests to simulate ImportError
    try:
        from strands import Agent  # type: ignore[import-not-found]
        from strands.models.openai import OpenAIModel  # type: ignore[import-not-found]
    except Exception as e:  # noqa: BLE001
        raise ModelGatewayError("strands is not installed") from e

    try:
        cfg = get_required_env()
    except Exception as e:  # noqa: BLE001
        raise ModelGatewayError(f"Invalid or missing environment: {e}") from e

    try:
        # Build underlying model using demo configuration style
        model = OpenAIModel(
            client_args={
                "api_key": cfg["api_key"],
                "base_url": cfg["base_url"],
            },
            model_id=cfg["model_name"],
            params={
                "max_tokens": 1000,
                "temperature": 0.7,
            },
        )

        agent = Agent(model=model, tools=[])

        return agent
    except Exception as e:  # noqa: BLE001
        raise ModelGatewayError(f"Failed to initialize agent: {e}") from e


def check_reachability(timeout_seconds: float = 5.0) -> bool:
    try:
        # Lazy import to avoid hard dependency when not needed
        import requests  # type: ignore[import-not-found]
    except Exception:
        return False

    cfg = get_required_env()
    try:
        resp = requests.options(cfg["base_url"], timeout=timeout_seconds)
        return 200 <= resp.status_code < 500
    except Exception:
        return False
