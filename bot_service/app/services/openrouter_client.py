import httpx

from app.core.config import settings

class OpenRouterError(RuntimeError):
	pass

def call_openrouter(prompt: str, timeout: float = 30.0) -> str:
	"""Отправляет OpenRouter запрос и возвращает ответ LLM"""
	api_key = settings.OPENROUTER_API_KEY
	if not api_key:
		raise OpenRouterError("OpenRouter API ключ не задан")

	request_url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json",
		"HTTP-Referer": settings.OPENROUTER_SITE_URL,
		"X-Title": settings.OPENROUTER_APP_NAME
	}
	payload = {
		"model": settings.OPENROUTER_MODEL,
		"messages": [{"role": "user", "content": prompt}]
	}

	try:
		with httpx.Client(timeout=timeout) as client:
			response = client.post(request_url, headers=headers, json=payload)

		if response.status_code >= 400:
			raise OpenRouterError(f"OpenRouter вернул {response.status_code}: {response.text}")

		body = response.json()
		content = body["choices"][0]["message"]["content"]

	except httpx.HTTPError as exc:
		raise OpenRouterError(f"Ошибка сети: {exc}") from exc
	except ValueError as exc:
		raise OpenRouterError("OpenRouter вернул не-json ответ") from exc
	except (KeyError, IndexError, TypeError) as exc:
		raise OpenRouterError("Openrouter вернул json неправильной структуры")

	return content.strip()
