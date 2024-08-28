import logging
import time

from aioredis import Redis, from_url
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from ..tools.logging import logger

logger = logging.getLogger("Application")


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url: str, rate_limit: int, rate_limit_period: int):
        super().__init__(app)
        self.redis_url = redis_url
        self.rate_limit = rate_limit
        self.rate_limit_period = rate_limit_period
        self.redis: Redis = None

    async def dispatch(self, request: Request, call_next):
        if not self.redis:
            self.redis = await from_url(self.redis_url, decode_responses=True)

        ip = request.client.host
        key = f"ratelimit:{ip}"

        current_time = int(time.time())
        start_time = current_time - self.rate_limit_period

        try:
            logger.info(f"Handling request from IP: {ip} at time: {current_time}")

            # Remove outdated requests
            removed = await self.redis.zremrangebyscore(key, 0, start_time)
            logger.info(f"Removed {removed} outdated requests for key: {key}")

            # Get current request count
            request_count = await self.redis.zcard(key)
            logger.info(f"Current request count for key {key}: {request_count}")

            if request_count >= self.rate_limit:
                logger.warning(f"Rate limit exceeded for key {key}")
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests from this IP. Please try again later."
                )

            # Add current request
            added = await self.redis.zadd(key, {current_time: current_time})
            logger.info(f"Added {added} requests at time {current_time} for key {key}")

            expiration_set = await self.redis.expire(key, self.rate_limit_period)
            logger.info(f"Set expiration for key {key}: {expiration_set}")

            response = await call_next(request)
            logger.info(f"Request handled successfully for IP: {ip}")
            return response

        except Exception as e:
            logger.error(f"Error in RateLimitMiddleware: {e}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )


class ExceptionLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled error: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal Server Error")
