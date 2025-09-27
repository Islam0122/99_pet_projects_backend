import aioredis

REDIS_TTL = 120  # 2 минуты

class RedisClient:
    def __init__(self, redis_url="redis://redis:6379/0"):
        self.redis_url = redis_url
        self.redis = None

    async def __aenter__(self):
        self.redis = await aioredis.from_url(self.redis_url, decode_responses=True)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.redis:
            await self.redis.close()

    async def get(self, key):
        val = await self.redis.get(key)
        if val:
            import json
            return json.loads(val)
        return None

    async def set(self, key, value, ex=REDIS_TTL):
        import json
        await self.redis.set(key, json.dumps(value), ex=ex)
