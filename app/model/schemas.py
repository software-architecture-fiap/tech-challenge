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
    user_agent: str
    ip_address: str
    os: str
    browser: str
    device: str
    comments: Optional[str] = None


class OrderProductBase(BaseModel):
    """
    Modelo Base para Dados de Produtos em um Pedido.

    Attributes:
        product_id (int): Identificador do produto.
        comment (Optional[str]): Comentário associado ao produto.
    """

    product_id: int
    comment: Optional[str] = None


class OrderProductCreate(OrderProductBase):
    """
    Modelo para Criação de um Produto em um Pedido.
    """

    pass


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