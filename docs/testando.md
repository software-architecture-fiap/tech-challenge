# Testando Aplicação no Swagger

Essa página irá mostrar para os nossos orientadores o processo completo de fazer os testes no nosso backend. Seguiremos
as etapas definidas no desafio.

## Entregáveis

### Entregável 1

1. [X] Documentação do sistema (DDD) com Event Storming, incluindo todos os passos/tipos de diagrama mostrados na aula 6 do
módulo de DDD, e utilizando a linguagem ubíqua, dos seguintes fluxos:

    1. [X] Realização do Pedido e Pagamento
    2. [X] Preparação e Entrega do Pedido

_É importante que os desenhos sigam os padrões utilizados na explicação._

#### Links das Entregas

- Documentação do Sistema [(DDD)](https://software-architecture-fiap.github.io/tech-challenge/ddd/)   
- Com [Event Storming](https://software-architecture-fiap.github.io/tech-challenge/event-storming/)

### Entregável 2

2. Uma Aplicação para todo o sistema de backend (monolito) que deverá ser desenvolvido seguindo os padrões apresentados
nas aulas:

    1. [X] Utilizando Arquitetura Hexagonal
    2. [X] API’s
        - [X] Cadastro do Cliente: Pode ser feito com ou sem cpf;
        - [X] Com cpf: Pode ser feito pela Rota [Create Customer](http://localhost:2000/docs#/customers/create_customer_customers_admin_post)
        - [X] Sem cpf: Pode ser feito pela Rota [Create Anonymous Customer](http://localhost:2000/docs#/customers/create_anonymous_customer_customers_anonymous_post)
        - [X] Identificação do Cliente via CPF: Se cadastrado com [Create Customer](http://localhost:2000/docs#/customers/create_customer_customers_admin_post)
        - [X] [Criar](http://localhost:2000/docs#/products/create_product_products__post), [Editar](http://localhost:2000/docs#/products/update_product_products__product_id__put) e [Remover](http://localhost:2000/docs#/products/delete_product_products__product_id__delete) Produtos: Necessário estar logado com Token;
        - [ ] Buscar Produtos por Categoria
        - [ ] Fake Checkout: apenas enviar os produtos escolhidos para a fila. O checkout é a finalização do pedido.
        - [ ] Listar os Pedidos
    3. [X] Banco de Dados à sua Escolha: Escolhemos o Postgres.
        - Inicialmente, deveremos trabalhar e organizar a fila dos pedidos apenas em um banco de dados.