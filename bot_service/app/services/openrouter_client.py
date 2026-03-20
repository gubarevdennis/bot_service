# bot_service/app/services/openrouter_client.py
import httpx
from app.core.config import settings

async def call_openrouter(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.OPENROUTER_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {settings.OPENROUTER_API_KEY}"},
            json={
                "model": settings.OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30.0
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]