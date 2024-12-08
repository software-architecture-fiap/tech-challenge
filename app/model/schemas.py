from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class CustomerBase(BaseModel):
    """
    Modelo Base para Dados de Clientes.

    Attributes:
        name (Optional[str]): Nome do cliente.
        email (Optional[str]): Email do cliente.
        cpf (Optional[str]): CPF do cliente.
    """

    name: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None

class CustomerCreate(CustomerBase):
    """
    Modelo para Criação de um Novo Cliente.

    Attributes:
        password (Optional[str]): Senha do cliente.
    """

    password: Optional[str] = None

class Customer(CustomerBase):
    """
    Modelo para Dados Completos do Cliente.

    Attributes:
        id (int): Identificador único do cliente.
    """

    id: int

    class Config:
        """
        Configurações específicas para o modelo Pydantic `Tracking`.
        """

        from_attributes = True

class CPFIdentify(BaseModel):
    """
    Modelo para Identificação por CPF.

    Attributes:
        cpf (str): CPF do cliente.
    """

    cpf: str

class Token(BaseModel):
    """
    Modelo para um Token de Autenticação.

    Attributes:
        access_token (str): Token de acesso.
        customer_id (int): Identificador do cliente associado ao token.
    """

    access_token: str
    customer_id: int

class TokenData(BaseModel):
    """
    Modelo para Dados do Token.

    Attributes:
        username (Optional[str]): Nome de usuário associado ao token.
    """

    username: Optional[str] = None

class ProductBase(BaseModel):
    """
    Modelo Base para Dados de Produtos.

    Attributes:
        name (str): Nome do produto.
        description (str): Descrição do produto.
        price (float): Preço do produto.
        category (str): Categoria do produto.
    """

    name: str
    description: str
    price: float
    category: str

    model_config = ConfigDict(from_attributes=True)

class Product(BaseModel):
    """
    Modelo para Dados Completos do Produto.

    Attributes:
        name (str): Nome do produto.
        description (str): Descrição do produto.
        price (float): Preço do produto.
        category (str): Categoria do produto.
    """

    name: str
    description: str
    price: float
    category: str
    enabled: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    """
    Modelo para Criação de um Novo Produto.

    Attributes:
        name (str): Nome do produto.
        description (str): Descrição do produto.
        price (float): Preço do produto.
        category_id (int): Identificador da categoria do produto.
    """

    name: str
    description: str
    price: float
    category_id: int

    model_config = ConfigDict(from_attributes=True)

class CategoryBase(BaseModel):
    """
    Modelo Base para Dados de Categorias.

    Attributes:
        name (str): Nome da categoria.
    """

    name: str

class CategoryCreate(CategoryBase):
    """
    Modelo para Criação de uma Nova Categoria.

    Attributes:
        description (Optional[str]): Descrição da categoria.
    """

    description: Optional[str] = None

class CategoryUpdate(BaseModel):
    """
    Modelo para Atualização de uma Categoria Existente.

    Attributes:
        name (Optional[str]): Nome da categoria.
        description (Optional[str]): Descrição da categoria.
    """

    name: Optional[str] = None
    description: Optional[str] = None

class Category(CategoryBase):
    """
    Modelo para Dados Completos da Categoria.

    Attributes:
        id (int): Identificador único da categoria.
        products (List[Product]): Lista de produtos pertencentes à categoria.
    """

    id: int
    products: List[Product] = []
    enabled: bool

    class Config:
        """
        Configurações específicas para o modelo Pydantic `Tracking`.
        """

        from_attributes = True

class OrderBase(BaseModel):
    """
    Modelo Base para Dados de Pedidos.

    Attributes:
        status (str): Status do pedido.
        user_agent (str): User-agent do pedido.
        ip_address (str): Endereço IP do pedido.
        os (str): Sistema operacional do pedido.
        browser (str): Navegador do pedido.
        device (str): Dispositivo do pedido.
        comments (Optional[str]): Comentários associados ao pedido.
    """

    status: str
    payment_status: str
    user_agent: str
    ip_address: str
    os: str
    browser: str
    device: str
    comments: Optional[str] = None

class ProductView(BaseModel):
    name: str
    description: str
    price: float
    category: Optional[CategoryBase] = None

class OrderProductBase(BaseModel):
    """
    Modelo Base para Dados de Produtos em um Pedido.

    Attributes:
        product_id (int): Identificador do produto.
        comment (Optional[str]): Comentário associado ao produto.
    """

    product_id: int
    comment: Optional[str] = None
    product: Optional[ProductView] = None

class OrderProductCreate(BaseModel):
    """
    Modelo para Criação de um Produto em um Pedido.
    """

    product_id: int
    comment: Optional[str] = None

class OrderProduct(OrderProductBase):
    """
    Modelo para Dados Completos de um Produto em um Pedido.

    Attributes:
        id (int): Identificador único do produto no pedido.
    """

    id: int

    class Config:
        """
        Configurações específicas para o modelo Pydantic `Tracking`.
        """

        from_attributes = True

class OrderCreate(OrderBase):
    """
    Modelo para Criação de um Novo Pedido.

    Attributes:
        customer_id (int): Identificador do cliente associado ao pedido.
        products (List[OrderProductCreate]): Lista de produtos associados ao pedido.
    """

    customer_id: int
    products: List[OrderProductCreate]
    email: Optional[str] = None
    total_price: float

class Order(OrderBase):
    """
    Modelo para Dados Completos do Pedido.

    Attributes:
        id (int): Identificador único do pedido.
        customer_id (int): Identificador do cliente associado ao pedido.
        created_at (datetime): Data e hora em que o pedido foi criado.
        updated_at (datetime): Data e hora em que o pedido foi atualizado.
        order_products (List[OrderProduct]): Lista de produtos associados ao pedido.
    """

    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime
    order_products: List[OrderProduct] = []

    class Config:
        """
        Configurações específicas para o modelo Pydantic `Tracking`.
        """

        from_attributes = True

class OrderResponse(BaseModel):
    """
    Modelo para Resposta de um Pedido.

    Attributes:
        id (int): Identificador único do pedido.
        customer_id (int): Identificador do cliente associado ao pedido.
    """

    id: int
    customer_id: int
    status: str
    created_at: datetime
    payment_status: str

    class Config:
        """
        Configurações específicas para o modelo Pydantic `Tracking`.
        """

        from_attributes = True

class OrderCustomerView(BaseModel):
    """
    Modelo para Visualizar um Pedido com Detalhes do Cliente.

    Attributes:
        id (int): Identificador único do pedido.
        customer_id (int): Identificador do cliente associado ao pedido.
        status (str): Status do pedido.
    """

    id: int
    customer_id: int
    status: str
    payment_status: str
    order_products: List[OrderProductBase] = []

    class Config:
        """
        Configurações específicas para o modelo Pydantic `Tracking`.
        """

        from_attributes = True

class TrackingCreate(BaseModel):
    """
    Modelo para Criação de um Rastreamento de Pedido.

    Attributes:
        status (str): Status do rastreamento.
        order_id (int): Identificador do pedido associado ao rastreamento.
    """

    status: str
    order_id: int

class Tracking(BaseModel):
    """
    Modelo para Dados Completos de Rastreamento de Pedido.

    Attributes:
        id (int): Identificador único do rastreamento.
        order_id (int): Identificador do pedido associado ao rastreamento.
        status (str): Status do rastreamento.
        created_at (datetime): Data e hora em que o rastreamento foi criado.
    """

    id: int
    order_id: int
    status: str
    created_at: datetime

    class Config:
        """
        Configurações específicas para o modelo Pydantic `Tracking`.
        """

        from_attributes = True

class UpdateOrderStatus(BaseModel):
    """
    Modelo para Atualização do Status de um Pedido.

    Attributes:
        status (str): Novo status do pedido.
    """

    status: str

class OrderStatus(str, Enum):
    PRONTO = "Pronto"
    EM_PREP = "Em preparação"
    RECEBIDO = "Recebido"
    FINALIZADO = "Finalizado"

class UpdateOrderPaymentStatus(BaseModel):
    """
    Modelo para Atualização do Status de um Pedido.

    Attributes:
        status (str): Novo status do pedido.
    """

    payment_status: str

class WebhookBase(BaseModel):
    id: int
    order_id: int
    status: str
    customer_id: int
    payment_status: str
    received_at: datetime

class WebhookCreate(BaseModel):
    order_id: int
    customer_id: int
    received_at: datetime

class WebhookResponse(BaseModel):
    order_id: int
    status: str
    customer_id: int
    payment_status: str
    received_at: datetime

class PaymentMethod(str, Enum):
    """Enumeração para Métodos de Pagamento."""
    CREDIT_CARD = "credit_card"
    PIX = "pix"
    BOLETO = "boleto"

class OrderPaymentBase(BaseModel):
    """
    Modelo Base para Dados de Pagamento de Pedido.

    Attributes:
        order_id (int): Identificador do pedido associado ao pagamento.
        status (str): Status do pagamento.
        payment_method (PaymentMethod): Método de pagamento utilizado.
        transaction_id (str): Identificador da transação.
        payment_provider (str): Nome do provedor de pagamento.
        amount (float): Valor do pagamento.
    """
    order_id: int
    status: str
    payment_method: PaymentMethod
    transaction_id: str
    payment_provider: str
    amount: float

class OrderPaymentCreate(BaseModel):
    """
    Modelo para Criação de um Pagamento de Pedido.

    Attributes:
        payment_method (PaymentMethod): Método de pagamento.
        amount (float): Valor do pagamento.
    """
    payment_method: PaymentMethod
    amount: float

class OrderPayment(OrderPaymentBase):
    """
    Modelo para Dados Completos de Pagamento de Pedido.

    Attributes:
        id (int): Identificador único do pagamento.
        created_at (datetime): Data e hora da criação do pagamento.
        updated_at (datetime): Data e hora da última atualização do pagamento.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Configurações específicas para o modelo Pydantic.
        """
        from_attributes = True

class MercadoPagoPaymentRequest(BaseModel):
    """
    Modelo para Requisição de Pagamento na API Mercado Pago.

    Attributes:
        transaction_amount (float): Valor total da transação.
        description (str): Descrição da transação.
        payment_method_id (str): Identificador do método de pagamento.
        payer_email (str): Email do pagador.
    """
    transaction_amount: float
    description: str
    payment_method_id: str
    payer_email: str

class MercadoPagoPaymentResponse(BaseModel):
    """
    Modelo para Resposta da API Mercado Pago.

    Attributes:
        id (str): Identificador único do pagamento.
        status (str): Status do pagamento.
        status_detail (str): Detalhes do status do pagamento.
        transaction_amount (float): Valor da transação.
        payment_method_id (str): Método de pagamento utilizado.
        payer_email (str): Email do pagador.
    """
    id: str
    status: str
    status_detail: str
    transaction_amount: float
    payment_method_id: str
    payer_email: str
