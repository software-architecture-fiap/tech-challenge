from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db.database import Base

class Customer(Base):
    """
    Representa um Cliente na Base de Dados.

    Attributes:
        id (int): Identificador único do cliente.
        name (str): Nome do cliente.
        email (str): Email do cliente.
        cpf (str): CPF do cliente.
        hashed_password (str): Senha do cliente criptografada.
        orders (relationship): Relacionamento com pedidos associados ao cliente.
    """

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    orders = relationship('Order', back_populates='customer')

class Product(Base):
    """
    Representa um Produto na Base de Dados.

    Attributes:
        id (int): Identificador único do produto.
        name (str): Nome do produto.
        description (str): Descrição do produto.
        price (float): Preço do produto.
        category_id (int): Identificador da categoria à qual o produto pertence.
        category (relationship): Relacionamento com a categoria do produto.
    """

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    enabled = Column(Boolean, default=True)

    category = relationship('Category', back_populates='products')
    order_products = relationship('OrderProduct', back_populates='product')

class Order(Base):
    """
    Representa um Pedido na Base de Dados.

    Attributes:
        id (int): Identificador único do pedido.
        status (str): Status do pedido.
        user_agent (str): User-agent do pedido.
        ip_address (str): Endereço IP do pedido.
        os (str): Sistema operacional do pedido.
        browser (str): Navegador do pedido.
        device (str): Dispositivo do pedido.
        comments (str): Comentários associados ao pedido.
        created_at (datetime): Data e hora em que o pedido foi criado.
        updated_at (datetime): Data e hora em que o pedido foi atualizado pela última vez.
        customer_id (int): Identificador do cliente associado ao pedido.
        customer (relationship): Relacionamento com o cliente associado ao pedido.
        order_items (relationship): Relacionamento com os itens do pedido.
        order_products (relationship): Relacionamento com os produtos do pedido.
        tracking (relationship): Relacionamento com o rastreamento do pedido.
        payments (relationship): Relacionamento com os pagamentos do pedido.
    """

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True, default='created')
    payment_status = Column(String, default='pendente')
    user_agent = Column(String)
    ip_address = Column(String)
    os = Column(String)
    browser = Column(String)
    device = Column(String)
    comments = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    customer = relationship('Customer', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')
    order_products = relationship('OrderProduct', back_populates='order')
    tracking = relationship('Tracking', back_populates='order')
    webhook = relationship('Webhook', back_populates='order')
    payments = relationship('OrderPayment', back_populates='order')

class OrderItem(Base):
    """
    Representa um Item em um Pedido.

    Attributes:
        id (int): Identificador único do item do pedido.
        order_id (int): Identificador do pedido ao qual o item pertence.
        product_id (int): Identificador do produto do item.
        comment (str): Comentário associado ao item do pedido.
        order (relationship): Relacionamento com o pedido ao qual o item pertence.
        product (relationship): Relacionamento com o produto do item.
    """

    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    comment = Column(String)

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product')

class OrderProduct(Base):
    """
    Representa um Produto Específico em um Pedido.

    Attributes:
        id (int): Identificador único do produto no pedido.
        order_id (int): Identificador do pedido ao qual o produto pertence.
        product_id (int): Identificador do produto.
        comment (str): Comentário associado ao produto do pedido.
        order (relationship): Relacionamento com o pedido ao qual o produto pertence.
        product (relationship): Relacionamento com o produto.
    """

    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    comment = Column(Text)

    order = relationship('Order', back_populates='order_products')
    product = relationship('Product', back_populates='order_products')

class OrderPayment(Base):
    """
    Representa um Pagamento associado a um Pedido.

    Attributes:
        id (int): Identificador único do pagamento.
        order_id (int): Identificador do pedido associado ao pagamento.
        status (str): Status do pagamento (e.g., 'approved', 'pending', 'failed').
        payment_method (str): Método de pagamento utilizado (e.g., 'credit_card', 'pix').
        transaction_id (str): Identificador da transação gerado pelo provedor de pagamento.
        payment_provider (str): Nome do provedor de pagamento (e.g., 'Mercado Pago').
        amount (float): Valor do pagamento.
        created_at (datetime): Data e hora em que o pagamento foi criado.
        updated_at (datetime): Data e hora em que o pagamento foi atualizado pela última vez.
    """

    __tablename__ = 'order_payments'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    status = Column(String, nullable=False, index=True)
    payment_method = Column(String, nullable=False)
    transaction_id = Column(String, unique=True, nullable=False)
    payment_provider = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    order = relationship('Order', back_populates='payments')

class Tracking(Base):
    """
    Representa o Rastreamento de um Pedido.

    Attributes:
        id (int): Identificador único do rastreamento.
        order_id (int): Identificador do pedido rastreado.
        status (str): Status do rastreamento.
        created_at (datetime): Data e hora em que o rastreamento foi criado.
        order (relationship): Relacionamento com o pedido rastreado.
    """

    __tablename__ = 'tracking'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    status = Column(String, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    order = relationship('Order', back_populates='tracking')

class Token(Base):
    """
    Representa um Token de Autenticação.

    Attributes:
        id (int): Identificador único do token.
        token (str): Valor do token.
        is_used (bool): Indica se o token foi utilizado.
        user_id (int): Identificador do cliente associado ao token.
        user (relationship): Relacionamento com o cliente associado ao token.
    """

    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    is_used = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('customers.id'))

    user = relationship('Customer')

class Category(Base):
    """
    Representa uma Categoria de Produtos.

    Attributes:
        id (int): Identificador único da categoria.
        name (str): Nome da categoria.
        products (relationship): Relacionamento com os produtos pertencentes à categoria.
    """

    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    enabled = Column(Boolean, default=True)
    products = relationship('Product', back_populates='category')

class Webhook(Base):
    __tablename__ = 'webhook'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    status = Column(String)
    payment_status = Column(String)
    received_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    customer_id = Column(Integer)
    order = relationship('Order', back_populates='webhook')
