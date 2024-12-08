import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from jose import jwt
from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload

from .mercadopago import MercadoPagoService
from ..model import models, schemas
from ..tools.logging import logger
from . import security

load_dotenv()

def create_token(db: Session, token: str, user_id: int) -> models.Token:
    """Cria um novo token para um usuário específico.

    Args:
        db (Session): Sessão do banco de dados.
        token (str): O token a ser criado.
        user_id (int): ID do usuário para o qual o token será criado.

    Returns:
        models.Token: O token criado.
    """
    logger.info(f'Creating token for user ID: {user_id}')
    db_token = models.Token(token=token, user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    logger.debug(f'Token created: {db_token.token}')
    return db_token

def mark_token_as_used(db: Session, token: str) -> models.Token:
    """Marca um token como usado.

    Args:
        db (Session): Sessão do banco de dados.
        token (str): O token a ser marcado como usado.

    Returns:
        models.Token: O token marcado como usado, ou None se o token não for encontrado.
    """
    logger.info(f'Marking token as used: {token}')
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    if not db_token:
        logger.warning(f'Token not found in database: {token}')
        return None
    db_token.is_used = True
    db.commit()
    db.refresh(db_token)
    logger.info(f'Token marked as used: {token}')
    return db_token

def is_token_used(db: Session, token: str) -> bool:
    """Verifica se um token já foi usado.

    Args:
        db (Session): Sessão do banco de dados.
        token (str): O token a ser verificado.

    Returns:
        bool: True se o token já foi usado, False caso contrário.
    """
    logger.debug(f'Checking if token is used: {token}')
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    if db_token and db_token.is_used:
        logger.debug(f'Token is used: {token}')
        return True
    logger.debug(f'Token is not used: {token}')
    return False

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """Cria um token de acesso JWT.

    Args:
        data (dict): Os dados a serem codificados no token.
        expires_delta (timedelta): O tempo até a expiração do token.

    Returns:
        str: O token de acesso JWT.
    """
    logger.debug('Creating access token')
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, security.SECRET_KEY, algorithm=security.ALGORITHM)
    logger.info('Access token created')
    return encoded_jwt

def get_user_by_email(db: Session, email: str) -> models.Customer:
    """Obtém um usuário pelo endereço de e-mail.

    Args:
        db (Session): Sessão do banco de dados.
        email (str): O endereço de e-mail do usuário.

    Returns:
        models.Customer: O usuário encontrado, ou None se nenhum usuário for encontrado.
    """
    logger.info(f'Fetching user with email: {email}')
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def create_user(db: Session, user: schemas.CustomerCreate) -> models.Customer:
    """Cria um novo usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user (schemas.CustomerCreate): Os dados do usuário a ser criado.

    Returns:
        models.Customer: O usuário criado.
    """
    logger.debug(f'Creating user with email: {user.email}')
    hashed_password = security.get_password_hash(user.password)
    db_user = models.Customer(name=user.name, email=user.email, cpf=user.cpf, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f'User created with ID: {db_user.id}')
    return db_user

def create_anonymous_customer(db: Session) -> models.Customer:
    """Cria um cliente anônimo.

    Args:
        db (Session): Sessão do banco de dados.

    Returns:
        models.Customer: O cliente anônimo criado.
    """
    logger.debug('Creating anonymous customer')
    anonymous_customer = models.Customer(name='Anonymous', email=None, cpf=None, hashed_password=None)
    db.add(anonymous_customer)
    db.commit()
    db.refresh(anonymous_customer)
    logger.info(f'Anonymous customer created with ID: {anonymous_customer.id}')
    return anonymous_customer

def get_customer_by_cpf(db: Session, cpf: str) -> models.Customer:
    """Obtém um cliente pelo CPF.

    Args:
        db (Session): Sessão do banco de dados.
        cpf (str): O CPF do cliente.

    Returns:
        models.Customer: O cliente encontrado, ou None se nenhum cliente for encontrado.
    """
    logger.debug(f'Fetching customer with CPF: {cpf}')
    return db.query(models.Customer).filter(models.Customer.cpf == cpf).first()

def create_admin_user(db: Session) -> None:
    """Cria um usuário administrador se ele ainda não existir.

    Os detalhes do administrador (nome, email, senha, CPF) devem ser fornecidos
    através de variáveis de ambiente: `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_CPF`, `ADMIN_NAME`.

    Args:
        db (Session): Sessão do banco de dados.

    Raises:
        Exception: Se houver algum erro ao criar o usuário administrador.
    """
    try:
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')
        admin_cpf = os.getenv('ADMIN_CPF')
        admin_name = os.getenv('ADMIN_NAME')

        if not all([admin_email, admin_password, admin_cpf, admin_name]):
            logger.error('Admin user details are not set in environment variables.')
            return

        logger.debug(f'Admin email: {admin_email}, Admin name: {admin_name}')

        user = db.query(models.Customer).filter(models.Customer.email == admin_email).first()
        if not user:
            hashed_password = security.get_password_hash(admin_password)
            admin_user = models.Customer(
                name=admin_name, email=admin_email, cpf=admin_cpf, hashed_password=hashed_password
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            logger.debug(f'Admin user created with email: {admin_email}')
        else:
            logger.debug(f'Admin user already exists with email: {admin_email}')
    except Exception as e:
        logger.error(f'Error creating admin user: {e}')

def get_customers_count(db: Session) -> int:
    """Obtém a contagem total de clientes.

    Args:
        db (Session): Sessão do banco de dados.

    Returns:
        int: O número total de clientes.
    """
    logger.info('Fetching total count of customers')
    return db.query(models.Customer).count()

def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    """Obtém um cliente pelo ID.

    Args:
        db (Session): Sessão do banco de dados.
        customer_id (int): ID do cliente.

    Returns:
        Optional[models.Customer]: O cliente encontrado ou None se nenhum cliente for encontrado.
    """
    logger.debug(f'Fetching customer with ID: {customer_id}')
    try:
        return db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    except Exception as e:
        logger.error(f'Error fetching customer: {e}')
        return None

def get_customers(db: Session, skip: int = 0, limit: int = 10) -> List[models.Customer]:
    """Obtém uma lista de clientes com paginação.

    Args:
        db (Session): Sessão do banco de dados.
        skip (int, optional): Número de registros a pular. Defaults to 0.
        limit (int, optional): Número máximo de registros a retornar. Defaults to 10.

    Returns:
        List[models.Customer]: Lista de clientes.
    """
    logger.debug(f'Fetching customers with skip: {skip}, limit: {limit}')
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    """Cria um novo cliente.

    Args:
        db (Session): Sessão do banco de dados.
        customer (schemas.CustomerCreate): Dados do cliente a ser criado.

    Returns:
        models.Customer: O cliente criado.
    """
    logger.debug(f'Creating customer with email: {customer.email}')
    db_customer = models.Customer(name=customer.name, email=customer.email, cpf=customer.cpf)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    logger.info(f'Customer created with ID: {db_customer.id}')
    return db_customer

def categorize_products(products: List[models.Product]) -> Dict[str, List[schemas.Product]]:
    """Categoriza produtos com base em sua categoria.

    Args:
        products (List[models.Product]): Lista de produtos a serem categorizados.

    Returns:
        Dict[str, List[schemas.Product]]: Dicionário com produtos categorizados por categoria.
    """
    categorized_products = {}
    for product in products:
        product_data = {
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'category': product.category.name,
        }

        if product.category.name not in categorized_products:
            categorized_products[product.category.name] = []

        categorized_products[product.category.name].append(schemas.Product(**product_data))

    return categorized_products

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Obtém um produto pelo ID.

    Args:
        db (Session): Sessão do banco de dados.
        product_id (int): ID do produto.

    Returns:
        Optional[models.Product]: O produto encontrado ou None se nenhum produto for encontrado.
    """
    logger.debug(f'Fetching product with ID: {product_id}')
    try:
        return db.query(models.Product).filter(models.Product.id == product_id, models.Product.enabled == True).first()
    except Exception as e:
        logger.error(f'Error fetching product: {e}')
        return None

def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[models.Product]:
    """Obtém uma lista de produtos com paginação.

    Args:
        db (Session): Sessão do banco de dados.
        skip (int, optional): Número de registros a pular. Defaults to 0.
        limit (int, optional): Número máximo de registros a retornar. Defaults to 10.

    Returns:
        List[models.Product]: Lista de produtos.
    """
    logger.debug(f'Fetching products with skip: {skip}, limit: {limit}')
    return (
        db.query(models.Product)
        .filter(models.Product.enabled == True)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """Cria um novo produto.

    Args:
        db (Session): Sessão do banco de dados.
        product (schemas.ProductCreate): Dados do produto a ser criado.

    Returns:
        models.Product: O produto criado.
    """
    logger.debug(f'Creating product with name: {product.name}')

    db_product = models.Product(
        name=product.name, description=product.description, price=product.price, category=product.category
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    logger.info(f'Product created with ID: {db_product.id}')

    return db_product

def update_product(db: Session, db_product: models.Product, product: schemas.ProductCreate) -> models.Product:
    """Atualiza as informações de um produto existente.

    Args:
        db (Session): Sessão do banco de dados.
        db_product (models.Product): Instância do produto existente no banco de dados.
        product (schemas.ProductCreate): Dados atualizados do produto.

    Returns:
        models.Product: O produto atualizado.
    """
    logger.debug(f'Updating product with name: {product.name}')
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.category = product.category
    db.commit()
    db.refresh(db_product)
    logger.info(f'Product updated with ID: {db_product.id}')
    return db_product

def delete_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Deleta um produto do banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        product_id (int): ID do produto a ser deletado.

    Returns:
        Optional[models.Product]: O produto deletado, ou None se não encontrado.
    """
    logger.debug(f'Deleting product with ID: {product_id}')
    try:
        db_product = db.query(
            models.Product
            ).filter(
                models.Product.id == product_id, 
                models.Product.enabled == True
                ).first()
        if db_product:
            db_product.enabled = False
            db.commit()
            logger.info(f'Product deleted: {db_product.name} - Category: {db_product.category}')
        else:
            logger.warning(f'Product not found: ID {product_id}')
        return db_product
    except Exception as e:
        logger.error(f'Error deleting product: {e}')
        return None

def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    """Cria um novo pedido no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        order (schemas.OrderCreate): Dados do pedido a ser criado.

    Returns:
        models.Order: O pedido criado.
    """
    logger.debug(f'Creating order for customer ID: {order.customer_id}')
    try:
        customer_id_int = order.customer_id
        db_order = models.Order(
            status=order.status,
            user_agent=order.user_agent,
            ip_address=order.ip_address,
            os=order.os,
            browser=order.browser,
            device=order.device,
            comments=order.comments,
            customer_id=customer_id_int,
            payment_status=order.payment_status,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        logger.info(f'Order created with ID: {db_order.id}')

        for product in order.products:
            product_id_int = product.product_id
            db_order_product = models.OrderProduct(
                order_id=db_order.id, product_id=product_id_int, comment=product.comment
            )
            db.add(db_order_product)
            db.commit()
            db.refresh(db_order_product)
            logger.info(f'Product {db_order_product.product_id} added to order {db_order.id}')

        create_tracking(db, db_order.id, db_order.status)

        return db_order
    except Exception as e:
        logger.error(f'Error creating order: {e}', exc_info=True)
        raise

def update_order_status(db: Session, order_id: int, status: str) -> Optional[models.Order]:
    """Atualiza o status de um pedido existente.

    Args:
        db (Session): Sessão do banco de dados.
        order_id (int): ID do pedido a ser atualizado.
        status (str): Novo status do pedido.

    Returns:
        Optional[models.Order]: O pedido atualizado, ou None se não encontrado.
    """
    logger.debug(f'Updating order status for order ID: {order_id} to {status}')
    try:
        db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if db_order:
            db_order.status = status
            db_order.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(db_order)
            logger.info(f'Order ID {db_order.id} status updated to {status}')
            create_tracking(db, db_order.id, status)
        return db_order
    except Exception as e:
        logger.error(f'Error updating order status: {e}', exc_info=True)
        raise

def update_order_payment_status(db: Session, order_id: int, payment_status: str) -> Optional[models.Order]:
    """Atualiza o status de pagamento de um pedido existente e cria um webhook se o status for 'Pago'.
    Args:
        db (Session): Sessão do banco de dados.
        order_id (int): ID do pedido a ser atualizado.
        status (str): Novo status do pedido.
    Returns:
        Optional[models.Order]: O pedido atualizado, ou None se não encontrado.
    """
    logger.debug(f'Updating order payment status for order ID: {order_id} to {payment_status}')
    try:
        db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if db_order:
            db_order.payment_status = payment_status
            db_order.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(db_order)
            logger.info(f'Order ID {db_order.id} payment status updated to {payment_status}')
            create_tracking(db, db_order.id, payment_status)

            if payment_status.lower() == "pago" or payment_status.lower() == "recusado":
                # Criando um schema do tipo WebhookCreate para passar para a função create_webhook
                webhook_data = schemas.WebhookCreate(
                    order_id=order_id,
                    received_at=datetime.now(timezone.utc),
                    customer_id=db_order.customer_id
                )
                create_webhook(db, webhook_data)
                logger.info(f'Creating a webhook entry for order ID: {db_order.id} at {webhook_data.received_at}')

        return db_order

    except Exception as e:
        logger.error(f'Error updating order payment status: {e}', exc_info=True)
        raise

def create_webhook(db: Session, webhook: schemas.WebhookCreate):

    logger.debug(f'Creating a webhook entry for order ID: {webhook.order_id}')
    try:
        order_search = db.query(models.Order).filter(models.Order.id == webhook.order_id).first()
        db_webhook = models.Webhook(
            order_id=order_search.id,
            received_at=webhook.received_at,
            status=order_search.status,
            payment_status=order_search.payment_status,
            customer_id=webhook.customer_id
        )
        db.query(models.Order).filter(models.Order.id == webhook.order_id).first()
        db.add(db_webhook)
        db.commit()
        db.refresh(db_webhook)
        logger.info(f'Webhook entry created with ID: {db_webhook.id}')
        return db_webhook
    except Exception as e:
        logger.error(f'Error creating tracking entry: {e}', exc_info=True)
        raise

def create_tracking(db: Session, order_id: int, status: str) -> models.Tracking:
    """Cria uma nova entrada de rastreamento para um pedido.

    Args:
        db (Session): Sessão do banco de dados.
        order_id (int): ID do pedido a ser rastreado.
        status (str): Status atual do pedido.

    Returns:
        models.Tracking: A entrada de rastreamento criada.
    """
    logger.debug(f'Creating tracking entry for order ID: {order_id} with status: {status}')
    try:
        db_tracking = models.Tracking(order_id=order_id, status=status, created_at=datetime.now(timezone.utc))
        db.add(db_tracking)
        db.commit()
        db.refresh(db_tracking)
        logger.info(f'Tracking entry created with ID: {db_tracking.id}')
        return db_tracking
    except Exception as e:
        logger.error(f'Error creating tracking entry: {e}', exc_info=True)
        raise

def get_orders(db: Session, skip: int = 0, limit: int = 10) -> List[models.Order]:
    """Obtém uma lista de pedidos com paginação.

    Args:
        db (Session): Sessão do banco de dados.
        skip (int, optional): Número de registros a pular. Defaults to 0.
        limit (int, optional): Número máximo de registros a retornar. Defaults to 10.

    Returns:
        List[models.Order]: Lista de pedidos.
    """
    logger.debug(f'Fetching orders with skip: {skip}, limit: {limit}')
    try:
        orders = (
            db.query(models.Order)
            .order_by(models.Order.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        logger.info('Orders fetched successfully')
        return orders
    except Exception as e:
        logger.error(f'Error fetching orders: {e}', exc_info=True)
        raise

def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    """Obtém um pedido pelo ID.

    Args:
        db (Session): Sessão do banco de dados.
        order_id (int): ID do pedido a ser obtido.

    Returns:
        Optional[models.Order]: O pedido correspondente, ou None se não encontrado.
    """

    logger.debug(f'Fetching order with ID: {order_id}')
    try:
        order = db.query(models.Order).options(
            joinedload(models.Order.order_products)
            .joinedload(models.OrderProduct.product)
            .joinedload(models.Product.category)  # Carregando a categoria associada ao produto
        ).filter(models.Order.id == order_id).first()

        logger.info('Order fetched successfully')
        return order
    except Exception as e:
        logger.error(f'Error fetching order: {e}', exc_info=True)
        raise

def get_categories(db: Session, skip: int = 0, limit: int = 10) -> List[schemas.Category]:
    """Obtém uma lista de categorias com paginação, incluindo os produtos associados.

    Args:
        db (Session): Sessão do banco de dados.
        skip (int, optional): Número de registros a pular. Defaults to 0.
        limit (int, optional): Número máximo de registros a retornar. Defaults to 10.

    Returns:
        List[schemas.Category]: Lista de categorias com seus produtos.
    """
    logger.debug(f'Fetching categories with skip: {skip}, limit: {limit}')
    categories = db.execute(
        text('SELECT id, name FROM categories LIMIT :limit OFFSET :skip WHERE enabled = true'), {'limit': limit, 'skip': skip}
    ).fetchall()

    category_list = []
    for category in categories:
        category_id = category.id
        products = db.execute(
            text('SELECT id, name, description, price FROM products WHERE category_id = :category_id AND enabled = true'),
            {'category_id': category_id},
        ).fetchall()

        product_list = [
            schemas.Product(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                category=category.name,
            )
            for product in products
        ]

        category_list.append(schemas.Category(id=category.id, name=category.name, products=product_list))

    return category_list

def get_category_with_products(db: Session, category_id: int) -> Optional[schemas.Category]:
    """Obtém uma categoria específica e seus produtos associados.

    Args:
        db (Session): Sessão do banco de dados.
        category_id (int): ID da categoria a ser obtida.

    Returns:
        Optional[schemas.Category]: A categoria com seus produtos, ou None se não encontrada.
    """
    logger.debug(f'Fetching category with ID: {category_id}')
    try:
        result = db.execute(
            text('SELECT * FROM categories WHERE id = :category_id AND enabled = true'), {'category_id': category_id}
        ).fetchone()
        if result:
            products = db.execute(
                text('SELECT * FROM products WHERE category_id = :category_id AND enabled = true'), {'category_id': category_id}
            ).fetchall()

            product_list = [schemas.Product(**dict(product)) for product in products]
            return schemas.Category(**dict(result), products=product_list)
    except Exception as e:
        logger.error(f'Error fetching category: {e}')
        return None

def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """Obtém uma categoria pelo ID.

    Args:
        db (Session): Sessão do banco de dados.
        category_id (int): ID da categoria a ser obtida.

    Returns:
        Optional[models.Category]: A categoria correspondente, ou None se não encontrada.
    """
    logger.debug(f'Fetching category with ID: {category_id}')
    try:
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        return category
    except Exception as e:
        logger.error(f'Error fetching category: {e}')
        return None

def update_category(
    db: Session, db_category: models.Category, category: schemas.CategoryCreate
) -> (Optional)[models.Category]:
    """Atualiza as informações de uma categoria existente.

    Args:
        db (Session): Sessão do banco de dados.
        db_category (models.Category): Instância da categoria existente no banco de dados.
        category (schemas.CategoryCreate): Dados atualizados da categoria.

    Returns:
        Optional[models.Category]: A categoria atualizada, ou None em caso de erro.
    """
    logger.debug(f'Updating category with ID: {db_category.id}')
    try:
        db_category.name = category.name
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        logger.error(f'Error updating category: {e}')
        return None

def delete_category(db: Session, db_category: models.Category) -> Optional[models.Category]:
    """Deleta uma categoria do banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        db_category (models.Category): Instância da categoria a ser deletada.

    Returns:
        Optional[models.Category]: A categoria deletada, ou None em caso de erro.
    """
    logger.debug(f'Deleting category with ID: {db_category.id}')
    try:
        db_category.enabled = False
        db.commit()
        return db_category
    except Exception as e:
        logger.error(f'Error deleting category: {e}')
        return None

def create_payment_preference(
    db: Session, order_id: int, payment_payload: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Cria uma preferência de pagamento no Mercado Pago.

    Args:
        db (Session): Sessão do banco de dados.
        order_id (int): ID do pedido.
        payment_payload (Dict[str, Any]): Dados da preferência de pagamento.

    Returns:
        Dict[str, Any]: Resposta da API Mercado Pago contendo a URL de pagamento.
    """
    try:
        logger.info(f"Criando preferência de pagamento para o pedido ID {order_id}")
        preference_response = MercadoPagoService.create_preference(payment_payload)
        
        # Valida a resposta
        if not preference_response or "init_point" not in preference_response:
            logger.error(f"Erro na criação da preferência de pagamento: {preference_response}")
            return None

        # Retorna dados necessários para o frontend
        return {
            "payment_url": preference_response["init_point"],
            "preference_id": preference_response["id"],
        }
    except Exception as e:
        logger.error(f"Erro ao criar preferência de pagamento para o pedido ID {order_id}: {e}", exc_info=True)
        raise
