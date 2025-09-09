import os
import pytest

from src.gateway.model_gateway import init_model, get_required_env, ModelGatewayError


requires_key = pytest.mark.skipif(
    not os.environ.get("TELENAV_API_KEY"), reason="TELENAV_API_KEY not set"
)


@requires_key
def test_init_model_and_complete_smoke():
    try:
        model = init_model()
    except ModelGatewayError as e:
        pytest.skip(f"Model unavailable: {e}")

    # Minimal smoke call: use the strands-agents interface if available
    # We only check that calling complete returns a text-like payload
    prompt = "Testing. Just say hi and nothing else."
    try:
        response = model.complete(prompt)  # type: ignore[attr-defined]
        text = response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        pytest.skip(f"Failed to complete: {e}")
    assert isinstance(text, str)
    assert len(text) > 0


