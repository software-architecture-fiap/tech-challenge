import time
from typing import Optional
from aioredis import Redis, from_url
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


from ..tools.logging import logger

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware para limitar a taxa de requisições por IP.

    Este middleware utiliza o Redis para armazenar o número de requisições feitas por um determinado IP
    em um período de tempo especificado. Se o número de requisições exceder o limite permitido, uma exceção
    HTTP 429 (Too Many Requests) é lançada.

    Attributes:
        app: A aplicação FastAPI à qual o middleware está associado.
        redis_url: A URL de conexão ao Redis.
        rate_limit: O número máximo de requisições permitidas por IP no período especificado.
        rate_limit_period: O período de tempo (em segundos) durante o qual as requisições são contadas.
        redis: Instância do cliente Redis.
    """

    def __init__(self, app, redis_url: str, rate_limit: int, rate_limit_period: int):
        """
        Inicializa o middleware com os parâmetros fornecidos.

        Args:
            app: A aplicação FastAPI à qual o middleware está associado.
            redis_url: A URL de conexão ao Redis.
            rate_limit: O número máximo de requisições permitidas por IP no período especificado.
            rate_limit_period: O período de tempo (em segundos) durante o qual as requisições são contadas.
        """
        super().__init__(app)
        self.redis_url = redis_url
        self.rate_limit = rate_limit
        self.rate_limit_period = rate_limit_period
        self.redis: Optional[Redis] = None

    async def dispatch(self, request: Request, call_next):
        """
        Manipula cada requisição, verificando se o IP ultrapassou o limite de requisições.

        Args:
            request: A requisição atual.
            call_next: Função que chama o próximo middleware ou endpoint.

        Returns:
            A resposta da aplicação, caso o limite de requisições não tenha sido excedido.

        Raises:
            HTTPException: Se o limite de requisições for excedido, uma exceção 429 é lançada.
        """
        if not self.redis:
            self.redis = await from_url(self.redis_url, decode_responses=True)

        ip = request.client.host
        key = f'ratelimit:{ip}'

        current_time = int(time.time())
        start_time = current_time - self.rate_limit_period

        try:
            logger.info(f'Recebendo Requisição do IP: {ip} no Tempo: {current_time}')

            # Remove Requisições Antigas
            removed = await self.redis.zremrangebyscore(key, 0, start_time)
            logger.info(f'Removi {removed} Requisições Antigas para a Chave: {key}')

            # Obtém o Número Atual de Requisições
            request_count = await self.redis.zcard(key)
            logger.info(f'Número Atual de Requisições para a Chave {key}: {request_count}')

            if request_count >= self.rate_limit:
                logger.warning(f'Limite de Requisições Excedido para a Chave {key}')
                raise HTTPException(status_code=429, detail='Muitas Requisições deste IP. Tente Novamente Mais Tarde!')

            # Adiciona a Requisição Atual
            added = await self.redis.zadd(key, {str(current_time): current_time})
            logger.info(f'Adicionadas {added} Requisições no Tempo {current_time} para a Chave {key}')

            # Define o Tempo de Expiração da Chave
            expiration_set = await self.redis.expire(key, self.rate_limit_period)
            logger.info(f'Tempo de Expiração Definido para a Chave {key}: {expiration_set}')

            response = await call_next(request)
            logger.info(f'Requisição Processada com Sucesso para o IP: {ip}')
            return response

        except Exception as e:
            logger.error(f'Erro no RateLimitMiddleware: {e}')
            raise HTTPException(status_code=500, detail='Erro Interno do Servidor!!!')

class ExceptionLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para capturar e registrar exceções não tratadas.

    Este middleware captura todas as exceções não tratadas durante o processamento das requisições
    e as registra no logger. Em seguida, retorna uma exceção HTTP 500 (Internal Server Error).

    Atributos:
        Nenhum.
    """

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except StarletteHTTPException as exc:
            logger.error(f"Erro HTTP: {exc.detail} | Status: {exc.status_code}")
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        except Exception as e:
            logger.exception(f"Erro interno: {e}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Erro Interno do Servidor"},
            )