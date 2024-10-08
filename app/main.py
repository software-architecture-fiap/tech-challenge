import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html

from .db.database import Base, SessionLocal, engine
from .middleware import ExceptionLoggingMiddleware
from .model import schemas
from .routers import auth, category, customer, order, product
from .services.repository import create_admin_user
from .services.security import get_current_user
from .tools.initialize_db import initialize_db
from .tools.logging import logger

# Criando todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)


def init_admin_user() -> None:
    """Inicializa o usuário admin e configura o banco de dados.

    Cria um usuário administrador e inicializa o banco de dados com dados padrão.

    Returns:
        None
    """
    db = SessionLocal()
    try:
        create_admin_user(db)
        initialize_db(db)
    finally:
        db.close()


app = FastAPI(on_startup=[init_admin_user])

logger.info('Application startup')

# Configuração do CORS
origins = [
    'http://localhost',
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Adicionar RateLimitMiddleware para proteger a rota de token
# app.add_middleware(RateLimitMiddleware, redis_url="/token", rate_limit=10, rate_limit_period=60)

# Incluindo os roteadores
app.add_middleware(ExceptionLoggingMiddleware)
app.include_router(auth.router)
app.include_router(customer.router, prefix='/customers', tags=['customers'])
app.include_router(product.router, prefix='/products', tags=['products'])
app.include_router(order.router, prefix='/orders', tags=['orders'])
app.include_router(category.router, prefix='/category', tags=['category'])


@app.get('/')
def read_root() -> dict:
    """Retorna o status operacional da aplicação.

    Returns:
        dict: Um dicionário com o status da aplicação.
    """
    logger.debug('Status endpoint accessed')
    return {'status': 'Operational'}


@app.get('/users/me', response_model=schemas.Customer)
def read_users_me(current_user: schemas.Customer = Depends(get_current_user)) -> schemas.Customer:
    """Retorna as informações do usuário atual.

    Args:
        current_user (schemas.Customer): O usuário atual obtido do token.

    Returns:
        schemas.Customer: As informações do usuário atual.
    """
    logger.debug(f'User endpoint accessed by {current_user.id}')
    return current_user


# Adiciona a rota para a documentação do ReDoc
@app.get('/redoc', include_in_schema=False)
async def redoc() -> str:
    """Retorna o HTML para a documentação do ReDoc.

    Returns:
        str: O HTML da documentação do ReDoc.
    """
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + ' - ReDoc',
        redoc_js_url='https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js',
    )


if __name__ == '__main__':
    uvicorn.run('app.main:app', host='127.0.0.1', port=2000, reload=True)
