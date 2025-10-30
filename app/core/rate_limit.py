import redis.asyncio as redis
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from config import settings

redis_client = None


async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding="utf-8",
            decode_responses=True
        )
    return redis_client


async def check_rate_limit(user_id: int, action: str = "create_point") -> bool:
    """
    Проверка rate limit для пользователя
    Ограничение: 5 точек в час для обычных пользователей
    """
    if not settings.RATE_LIMIT_ENABLED:
        return True

    client = await get_redis()
    key = f"rate_limit:{action}:{user_id}"

    # Получаем текущее количество
    current = await client.get(key)

    if current is None:
        # Первый запрос - устанавливаем счетчик на 1 час
        await client.setex(key, 3600, 1)
        return True

    current_count = int(current)

    if current_count >= settings.RATE_LIMIT_POINTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Превышен лимит создания точек. Максимум {settings.RATE_LIMIT_POINTS} в час."
        )

    # Инкрементируем счетчик
    await client.incr(key)
    return True