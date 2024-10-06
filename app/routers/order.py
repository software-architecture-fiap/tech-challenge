from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..model import schemas
from ..model.schemas import OrderStatus
from ..services import repository, security
from ..tools.logging import logger

router = APIRouter()


@router.post('/', response_model=schemas.OrderResponse)
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
        raise HTTPException(status_code=500, detail='Erro Interno do Servidor')


@router.put('/{order_id}/status', response_model=schemas.OrderResponse)
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
        logger.warning(f'Formato de ID do pedido inválido: {order_id}')
        raise HTTPException(status_code=400, detail='Formato de ID do pedido inválido')

    try:
        db_order = repository.update_order_status(db, order_id=order_id_int, status=update_data.status)
        if db_order is None:
            logger.warning(f'Pedido não encontrado: {order_id}')
            raise HTTPException(status_code=404, detail='Pedido não encontrado')
        logger.info(f'Status do ID do pedido {order_id} atualizado para {update_data.status}')
        return db_order
    except Exception as e:
        logger.error(f'Erro ao atualizar o status do pedido: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail='Erro Interno do Servidor')


@router.get('/', response_model=Dict[str, List[schemas.OrderResponse]])
def read_orders(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> Dict[str, List[schemas.OrderResponse]]:
    """Recupera uma lista de pedidos com paginação.

    Args:
        skip (int): O número de registros a serem ignorados.
        limit (int): O número máximo de registros a serem retornados.
        db (Session): A sessão do banco de dados.
        current_user (schemas.Customer): O usuário autenticado atualmente.

    Returns:
        Dict[str, List[schemas.OrderResponse]]: Um dicionário contendo uma lista de pedidos.
    """
    logger.info('Endpoint de leitura de pedidos chamado')
    try:
        orders = repository.get_orders(db, skip=skip, limit=limit)
        filtered_orders = [order for order in orders if order.status != 'Finalizado']
        logger.info('Pedidos recuperados com sucesso')
        return {'orders': filtered_orders}
    except Exception as e:
        logger.error(f'Erro ao recuperar os pedidos: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail='Erro Interno do Servidor')


@router.get('/{order_id}', response_model=schemas.OrderCustomerView)
def read_order(
    order_id: str, db: Session = Depends(get_db), current_user: schemas.Customer = Depends(security.get_current_user)
) -> schemas.OrderCustomerView:
    """Recupera um pedido específico pelo seu ID.

    Args:
        order_id (str): O ID do pedido a ser recuperado.
        db (Session): A sessão do banco de dados.
        current_user (schemas.Customer): O usuário autenticado atualmente.

    Raises:
        HTTPException: Se o formato do ID do pedido for inválido, o pedido não for encontrado, ou ocorrer um erro.

    Returns:
        schemas.OrderCustomerView: Os detalhes do pedido.
    """
    logger.info(f'Endpoint de leitura de pedido chamado para o ID do pedido: {order_id}')
    try:
        order_id_int = order_id
    except (ValueError, IndexError):
        logger.warning(f'Formato de ID do pedido inválido: {order_id}')
        raise HTTPException(status_code=400, detail='Formato de ID do pedido inválido')

    try:
        db_order = repository.get_order(db, order_id=order_id_int)
        if db_order is None:
            logger.warning(f'Pedido não encontrado: {order_id}')
            raise HTTPException(status_code=404, detail='Pedido não encontrado')
        logger.info(f'Pedido recuperado com sucesso para o ID do pedido: {order_id}')
        return db_order
    except Exception as e:
        logger.error(f'Erro ao recuperar o pedido: {e}', exc_info=True)
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
        raise HTTPException(status_code=500, detail='Erro Interno do Servidor')


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
        db_order = repository.update_order_payment_status(db, order_id=order_id_int, payment_status=update_data.payment_status)
        if db_order is None:
            logger.warning(f'Pedido não encontrado: {order_id}')
            raise HTTPException(status_code=404, detail='Pedido não encontrado')
        logger.info(f'Status de pagamento do pedido de ID {order_id} atualizado para {update_data.payment_status}')
        return db_order
    except Exception as e:
        logger.error(f'Erro ao atualizar o status de pagamento do pedido: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail='Erro Interno do Servidor')


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
