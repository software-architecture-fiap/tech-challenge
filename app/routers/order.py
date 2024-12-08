from typing import Dict, List, Union, Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..db.database import get_db
from ..model import schemas
from ..model.schemas import OrderStatus
from ..services import repository, security
from ..tools.logging import logger

router = APIRouter()

INTERNAL_SERVER_ERROR_MSG = "Erro Interno do Servidor"
INVALID_ORDER_ID_MSG = "Formato de ID do pedido inválido"
REQUEST_NOT_FOUND_MSG = "Pedido não encontrado"

@router.post('', response_model=Dict[str, Any])
def create_order_with_payment(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: Optional[schemas.Customer] = Depends(security.get_optional_user),
) -> Dict[str, Any]:
    """
    Cria um novo pedido e gera o link de pagamento.
    """
    logger.info("Endpoint de criação de pedido chamado")

    try:
        # Determinar o email do cliente
        if current_user:
            customer_email = current_user.email
        else:
            # Usar email mock se não for fornecido
            customer_email = order.email or f"pagador_teste_{int(datetime.now().timestamp())}@exemplo.com"
            logger.warning(f"Email não fornecido. Usando mock: {customer_email}")

        # Criação do pedido
        db_order = repository.create_order(db=db, order=order)
        logger.info(f"Pedido criado com sucesso. ID: {db_order.id}")

        # Criação da preferência de pagamento
        payment_payload = {
            "items": [
                {
                    "title": f"Pedido {db_order.id}",
                    "quantity": 1,
                    "unit_price": order.total_price,
                    "currency_id": "BRL",
                }
            ],
            "payer": {"email": customer_email},
        }
        payment_preference = repository.create_payment_preference(db=db, order_id=db_order.id, payment_payload=payment_payload)

        if not payment_preference:
            logger.warning(f"Erro ao criar a preferência de pagamento para o pedido ID {db_order.id}")
            raise HTTPException(status_code=500, detail="Erro ao criar a preferência de pagamento")

        logger.info(f"Preferência de pagamento gerada com sucesso para o pedido ID {db_order.id}")

        # Retorno consolidado
        return {
            "order": {
                "id": db_order.id,
                "status": db_order.status,
                "payment_status": db_order.payment_status,
                "created_at": db_order.created_at,
            },
            "payment": {
                "payment_url": payment_preference["payment_url"],
                "preference_id": payment_preference["preference_id"],
            },
        }

    except Exception as e:
        logger.error(f"Erro ao criar pedido ou preferência de pagamento: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro Interno do Servidor")

@router.patch('/{order_id}/status', response_model=schemas.OrderResponse)
def update_order_status(
    order_id: str,
    update_data: schemas.UpdateOrderStatus,
    db: Session = Depends(get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> schemas.OrderResponse:
    """Atualiza o status de um pedido existente.

    Args:
        order_id (str): O ID do pedido a ser atualizado.
        update_data (schemas.UpdateOrderStatus): Os dados de atualização de status.
        db (Session): A sessão do banco de dados.
        current_user (schemas.Customer): O usuário autenticado atualmente.

    Raises:
        HTTPException: Se o formato do ID do pedido for inválido, o pedido não for encontrado, ou ocorrer um erro.

    Returns:
        schemas.OrderResponse: O pedido atualizado.
    """
    logger.info(
        f'Endpoint de atualização de status do pedido chamado para o ID do pedido: {order_id} com status: '
        f'{update_data.status}'
    )
    try:
        update_data.status = OrderStatus(update_data.status)
    except (ValueError, IndexError):
        logger.warning(f'Status {update_data.status} não é permitido')
        raise HTTPException(status_code=422, detail='Status não permitido')

    try:
        order_id_int = order_id
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail=INVALID_ORDER_ID_MSG)

    try:
        db_order = repository.update_order_status(db, order_id=order_id_int, status=update_data.status)
        if db_order is None:
            logger.warning(f'Pedido não encontrado: {order_id}')
            raise HTTPException(status_code=404, detail=REQUEST_NOT_FOUND_MSG)
        logger.info(f'Status do ID do pedido {order_id} atualizado para {update_data.status}')
        return db_order
    except Exception as e:
        logger.error(f'Erro ao atualizar o status do pedido: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_MSG)

@router.get('', response_model=Union[Dict[str, List[schemas.OrderResponse]], schemas.OrderCustomerView])
def read_orders_or_order(
    order_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> Union[Dict[str, List[schemas.OrderResponse]], schemas.OrderCustomerView]:
    """
    Recupera uma lista de pedidos com paginação ou um pedido específico pelo ID.

    Args:
        order_id (Optional[str]): ID do pedido a ser recuperado. Se não fornecido, retorna uma lista paginada.
        skip (int): Número de registros a serem ignorados.
        limit (int): Número máximo de registros a serem retornados.
        db (Session): Sessão do banco de dados.
        current_user (schemas.Customer): Usuário autenticado atualmente.

    Raises:
        HTTPException: Se o ID do pedido for inválido, o pedido não for encontrado, ou ocorrer um erro.

    Returns:
        Union[Dict[str, List[schemas.OrderResponse]], schemas.OrderCustomerView]: Detalhes de um pedido ou uma lista de pedidos.
    """
    if order_id:
        logger.info(f'Buscando pedido com ID: {order_id}')
        try:
            order_id_int = order_id
        except (ValueError, IndexError):
            logger.warning(f'Formato de ID do pedido inválido: {order_id}')
            raise HTTPException(status_code=400, detail='Formato de ID do pedido inválido')

        try:
            db_order = repository.get_order(db, order_id=order_id_int)
            if db_order is None:
                logger.warning(f'Pedido com ID {order_id} não encontrado')
                raise HTTPException(status_code=404, detail='Pedido não encontrado')
            logger.info(f'Pedido recuperado com sucesso para o ID: {order_id}')
            return db_order
        except Exception as e:
            logger.error(f'Erro ao recuperar o pedido: {e}', exc_info=True)
            raise HTTPException(status_code=500, detail='Erro Interno do Servidor')

    logger.info(f'Buscando lista de pedidos com paginação skip={skip}, limit={limit}')
    try:
        orders = repository.get_orders(db, skip=skip, limit=limit)
        filtered_orders = [order for order in orders if order.status != 'Finalizado']
        logger.info('Pedidos recuperados com sucesso')
        return {'orders': filtered_orders}
    except Exception as e:
        logger.error(f'Erro ao recuperar os pedidos: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail='Erro Interno do Servidor')

@router.post('/checkout', response_model=schemas.OrderResponse)
def fake_checkout(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> schemas.OrderResponse:
    """Cria um novo pedido como parte de um processo de checkout fictício.

    Args:
        order (schemas.OrderCreate): Os dados do pedido a ser criado.
        db (Session): A sessão do banco de dados.
        current_user (schemas.Customer): O usuário autenticado atualmente.

    Raises:
        HTTPException: Se ocorrer um erro durante o checkout fictício.

    Returns:
        schemas.OrderResponse: O pedido criado.
    """
    logger.info('Endpoint de checkout fictício chamado')
    try:
        db_order = repository.create_order(db=db, order=order)
        logger.info('Pedido de checkout criado com sucesso')
        return db_order
    except Exception as e:
        logger.error(f'Erro durante o checkout fictício: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_MSG)

@router.post('/webhook', response_model=schemas.WebhookResponse)
def create_webhook(
    webhook: schemas.WebhookCreate,
    db: Session = Depends(get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> schemas.WebhookResponse:

    logger.info('Endpoint de criação de webhook chamado')
    try:
        db_webhook = repository.create_webhook(db=db, webhook=webhook)
        logger.info(
            f'Endpoint de atualização de status do pedido chamado para o ID de pedido: {webhook.order_id}'
        )
        return db_webhook
    except Exception as e:
        logger.error(f'Erro ao criar o pedido: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail='Erro Interno do Servidor')

@router.post('/payment', response_model=schemas.OrderResponse)
def process_order_payment(
    order_id: str,
    payment_payload: Dict,
    db: Session = Depends(get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> schemas.OrderResponse:
    """
    Processa o pagamento de um pedido usando o Mercado Pago.

    Args:
        order_id (str): O ID do pedido para o qual o pagamento será processado.
        payment_payload (Dict): Os dados do pagamento enviados pelo cliente.
        db (Session): A sessão do banco de dados.
        current_user (schemas.Customer): O usuário autenticado atualmente.

    Raises:
        HTTPException: Se o formato do ID do pedido for inválido, o pedido não for encontrado, ou ocorrer um erro.

    Returns:
        schemas.OrderResponse: O pedido atualizado com o status do pagamento.
    """
    logger.info(f"Endpoint de pagamento chamado para o ID do pedido: {order_id}")
    try:
        # Valida o formato do ID do pedido
        order_id_int = order_id
    except (ValueError, IndexError):
        logger.warning(f"Formato de ID do pedido inválido: {order_id}")
        raise HTTPException(status_code=400, detail="Formato de ID do pedido inválido")

    try:
        # Chama a função de processamento de pagamento no repository
        db_order = repository.process_payment(db=db, order_id=order_id_int, payment_payload=payment_payload)
        if db_order is None:
            logger.warning(f"Pedido não encontrado: {order_id}")
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        logger.info(f"Pagamento processado com sucesso para o ID do pedido: {order_id}")
        return db_order
    except Exception as e:
        logger.error(f"Erro ao processar o pagamento do pedido {order_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro Interno do Servidor")

@router.patch('/{order_id}/payment', response_model=schemas.OrderResponse)
def update_order_payment_status(
    order_id: str,
    update_data: schemas.UpdateOrderPaymentStatus,
    db: Session = Depends(get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> schemas.OrderResponse:
    """Atualiza o status de pagamento um pedido criado.

    Args:
        order_id (str): O ID do pedido a ser atualizado.
        update_data (schemas.UpdateOrderPaymentStatus): Os dados de atualização de status de pagamento.
        db (Session): A sessão do banco de dados.
        current_user (schemas.Customer): O usuário autenticado atualmente.

    Raises:
        HTTPException: Se o formato do ID do pedido for inválido, o pedido não for encontrado, ou ocorrer um erro.

    Returns:
        schemas.OrderResponse: O pedido atualizado.
    """
    logger.info(
        f'Endpoint de atualização de status do pedido chamado para o ID do pedido: {order_id} com status: '
        f'{update_data.payment_status}'
    )
    try:
        order_id_int = order_id
    except (ValueError, IndexError):
        logger.warning(f'Formato de ID do pedido inválido: {order_id}')
        raise HTTPException(status_code=400, detail='Formato de ID do pedido inválido')

    try:
        db_order = repository.update_order_payment_status(
            db, order_id=order_id_int, payment_status=update_data.payment_status
        )
        if db_order is None:
            logger.warning(f'Pedido não encontrado: {order_id}')
            raise HTTPException(status_code=404, detail='Pedido não encontrado')
        logger.info(f'Status de pagamento do pedido de ID {order_id} atualizado para {update_data.payment_status}')
        return db_order
    except Exception as e:
        logger.error(f'Erro ao atualizar o status de pagamento do pedido: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail='Erro Interno do Servidor')

@router.post('', response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> schemas.OrderResponse:
    """Cria um novo pedido com os dados fornecidos.

    Args:
        order (schemas.OrderCreate): Os dados do pedido a ser criado.
        db (Session): A sessão do banco de dados.
        current_user (schemas.Customer): O usuário autenticado atualmente.

    Raises:
        HTTPException: Se ocorrer um erro ao criar o pedido.

    Returns:
        schemas.OrderResponse: O pedido criado.
    """
    logger.info('Endpoint de criação de pedido chamado')
    try:
        db_order = repository.create_order(db=db, order=order)
        logger.info('Pedido criado com sucesso')
        return db_order
    except Exception as e:
        logger.error(f'Erro ao criar o pedido: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_MSG)

#@router.get('/', response_model=Dict[str, List[schemas.OrderResponse]])
#def read_orders(
#    skip: int = 0,
#    limit: int = 10,
#    db: Session = Depends(get_db),
#    current_user: schemas.Customer = Depends(security.get_current_user),
#) -> Dict[str, List[schemas.OrderResponse]]:
#    """Recupera uma lista de pedidos com paginação.
#
#    Args:
#        skip (int): O número de registros a serem ignorados.
#        limit (int): O número máximo de registros a serem retornados.
#        db (Session): A sessão do banco de dados.
#        current_user (schemas.Customer): O usuário autenticado atualmente.
#
#    Returns:
#        Dict[str, List[schemas.OrderResponse]]: Um dicionário contendo uma lista de pedidos.
#    """
#    logger.info('Endpoint de leitura de pedidos chamado')
#    try:
#        orders = repository.get_orders(db, skip=skip, limit=limit)
#        filtered_orders = [order for order in orders if order.status != 'Finalizado']
#        logger.info('Pedidos recuperados com sucesso')
#        return {'orders': filtered_orders}
#    except Exception as e:
#        logger.error(f'Erro ao recuperar os pedidos: {e}', exc_info=True)
#        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_MSG)
#
#@router.get('/{order_id}', response_model=schemas.OrderCustomerView)
#def read_order(
#    order_id: str, db: Session = Depends(get_db), current_user: schemas.Customer = Depends(security.get_current_user)
#) -> schemas.OrderCustomerView:
#    """Recupera um pedido específico pelo seu ID.
#
#    Args:
#        order_id (str): O ID do pedido a ser recuperado.
#        db (Session): A sessão do banco de dados.
#        current_user (schemas.Customer): O usuário autenticado atualmente.
#
#    Raises:
#        HTTPException: Se o formato do ID do pedido for inválido, o pedido não for encontrado, ou ocorrer um erro.
#
#    Returns:
#        schemas.OrderCustomerView: Os detalhes do pedido.
#    """
#    logger.info(f'Endpoint de leitura de pedido chamado para o ID do pedido: {order_id}')
#    try:
#        order_id_int = order_id
#    except (ValueError, IndexError):
#        logger.warning(f'Formato de ID do pedido inválido: {order_id}')
#        raise HTTPException(status_code=400, detail='Formato de ID do pedido inválido')
#
#    try:
#        db_order = repository.get_order(db, order_id=order_id_int)
#        if db_order is None:
#            logger.warning(f'Pedido não encontrado: {order_id}')
#            raise HTTPException(status_code=404, detail='Pedido não encontrado')
#        logger.info(f'Pedido recuperado com sucesso para o ID do pedido: {order_id}')
#        return db_order
#    except Exception as e:
#        logger.error(f'Erro ao recuperar o pedido: {e}', exc_info=True)
#        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_MSG)
