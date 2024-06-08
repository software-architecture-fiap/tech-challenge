from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import customer, product, order, auth
from .security import get_current_user
from . import schemas
from .middleware import RateLimitMiddleware
from .logging_config import logger

# Criando todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

logger.info("Application startup")

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    # Adicione outras origens permitidas aqui
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar RateLimitMiddleware para proteger a rota de token
app.add_middleware(RateLimitMiddleware, redis_url="/token", rate_limit=10, rate_limit_period=60)

# Incluindo os roteadores
app.include_router(auth.router)
app.include_router(customer.router, prefix="/customers", tags=["customers"])
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(order.router, prefix="/orders", tags=["orders"])

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the food ordering system!"}

@app.get("/users/me", response_model=schemas.Customer)
def read_users_me(current_user: schemas.Customer = Depends(get_current_user)):
    logger.info(f"User endpoint accessed by {current_user.id}")
    return current_user
