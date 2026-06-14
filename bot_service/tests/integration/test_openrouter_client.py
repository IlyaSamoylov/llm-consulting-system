import pytest
import respx
import httpx
import json

from app.core.config import settings
from app.services.openrouter_client import call_openrouter

@pytest.mark.integration
@respx.mock
def test_call_openrouter_returns_text_and_sends_request() -> None:
	route = respx.post(f"{settings.OPENROUTER_BASE_URL}/chat/completions").mock(
		return_value=httpx.Response(
			200,
			json={
				"choices": [
					{
						"message": {
							"content": "Тестовый ответ OpenRouter"
						}
					}
				]
			},
		)
	)

	result = call_openrouter("Привет", timeout=5.0)

	assert result == "Тестовый ответ OpenRouter"
	assert route.called
	assert route.call_count == 1

	request = route.calls[0].request
	assert request.headers["Authorization"] == f"Bearer {settings.OPENROUTER_API_KEY}"
	assert request.headers["HTTP-Referer"] == settings.OPENROUTER_SITE_URL
	assert request.headers["X-Title"] == settings.OPENROUTER_APP_NAME

	payload = json.loads(request.content.decode())
	assert payload["model"] == settings.OPENROUTER_MODEL
	assert payload["messages"] == [{"role": "user", "content": "Привет"}]