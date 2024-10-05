# Novas Rotas

## Checkout Pedido

- **Descrição:** Endpoint responsável por receber os produtos solicitados e retornar a identificação do pedido gerado.
- **Método:** `POST`
- **Endpoint:** `/orders/checkout`
- **Request Body:**
    ```json
    {
      "status": "string",
      "payment_status": "string",
      "user_agent": "string",
      "ip_address": "string",
      "os": "string",
      "browser": "string",
      "device": "string",
      "comments": "string",
      "customer_id": 0,
      "products": [
        {
          "product_id": 0,
          "comment": "string"
        }
      ]
    }
    ```
- **Response Body:**

    ```json
    {
      "id": 0,
      "customer_id": 0,
      "status": "string",
      "created_at": "2024-10-03T14:25:43.242Z",
      "payment_status": "string"
    }
    ```

---

## Consultar Status de Pagamento

- **Descrição:** Consulta o status de pagamento de um pedido para verificar se o pagamento foi aprovado ou não.
- **Método:** `GET`
- **Endpoint:** `/orders/{order_id}`
- **Parâmetro:** `order_id` (string): Identificação única do pedido.
- **Exemplo de Request:** `GET /orders/1`
- **Response Body:**

    ```json
    {
      "id": 1,
      "customer_id": 1,
      "status": "Finalizado",
      "payment_status": "pago",
      "order_products": [
        {
          "product_id": 1,
          "comment": "Sem cebola",
          "product": {
            "name": "Sanduíche de Frango Grelhado",
            "description": "Grilled chicken sandwich with lettuce",
            "price": 15,
            "category": {
              "name": "Sanduíches"
            }
          }
        }
      ]
    }
    ```

---

## Confirmação de Pagamento

- **Descrição:** Recebe notificações de pagamento aprovadas ou recusadas via webhook. Ele é disparado automáticamente uma vez que um pedido sofre alteração em seu status de pagamento.
- **Método:** `POST`
- **Endpoint:** `/orders/webhook`
- **Request Body:**

    ```json
    {
      "order_id": 0,
      "customer_id": 0,
      "received_at": "2024-10-03T14:40:48.732Z"
    }
    ```
- **Response Body:**

    ```json
    {
      "order_id": 0,
      "status": "string",
      "customer_id": 0,
      "payment_status": "string",
      "received_at": "2024-10-03T14:40:48.733Z"
    }
    ```

---

## Listar pedidos

- **Descrição:** Retorna a lista de pedidos com suas descrições, ordenados por:
    1. Regra de ordenação: `Pronto` > `Em Preparação` > `Recebido`;
    2. Pedidos mais antigos primeiro, baseado na o atributo `created_at`;
    3. Pedidos com status `Finalizado` não devem aparecer.
- **Método:** `GET`
- **Endpoint:** `/orders`
- **Response Body:**

    ```json
    {
      "orders": [
        {
          "id": 5,
          "customer_id": 1,
          "status": "Recebido",
          "created_at": "2024-09-12T19:06:46.240199",
          "payment_status": "pago"
        },
        {
          "id": 6,
          "customer_id": 1,
          "status": "Recebido",
          "created_at": "2024-09-12T19:12:34.059608",
          "payment_status": "pago"
        },
        {
          "id": 8,
          "customer_id": 1,
          "status": "Recebido",
          "created_at": "2024-09-12T19:20:01.736862",
          "payment_status": "pago"
        }
      ]
    }
    ```

---

## Atualizar Status do Pedido

- **Descrição:** Permite a atualização do status de um pedido específico.
- **Método:** `PUT`
- **Endpoint:** `/orders/{order_id}/status`
- **Parâmetro:** `order_id` (string): Identificação única do pedido.
- **Request Body:**

    ```json
    {
      "status": "string"
    }
    ```
  
- **Response Body:**

    ```json
    {
      "id": 0,
      "customer_id": 0,
      "status": "string",
      "created_at": "2024-10-03T14:47:37.710Z",
      "payment_status": "string"
    }
    ```

## Atualizar Status de Pagamento

- **Descrição:** Permite a atualização do status de pagamento de um pedido.
- **Método:** `PATCH`
- **Endpoint:** `/orders/{order_id}/payment`
- **Parâmetro:** `order_id` (string): Identificação única do pedido.
- **Request Body:**

    ```json
    {
      "payment_status": "string"
    }
    ```

- **Response Body:**

    ```json
    {
      "id": 0,
      "customer_id": 0,
      "status": "string",
      "created_at": "2024-10-03T14:50:06.223Z",
      "payment_status": "string"
    }
    ```
