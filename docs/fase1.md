# Passo a Passo para Testar o Backend

## :material-foot-print: Passos
Nessa documentação iremos te mostrar os Passos que você deve dar em direção aos testes. Isso irá lhe proporcionar uma
melhor experiência durante os teste. Abaixo, clique em cada uma das caixas de passos para seguir com cada etapa.

???- note "Passo 01: Login for Access Token"
    A primeira coisa que deve ser feita é a criação de um User Admin para o iniciar o Teste do Backend. 
    Você poderá fazer isso atráves do Swagger em
    [Login for Access Token](http://localhost:2000/docs#/default/login_for_access_token_token_post).

    ![image](assets/t01.png)
    
    Os campos **username** e **password** são obrigatórios! Preencha-os e Clique em Execute. Isso te dará acesso às
    etapas que exigem camadas de autenticação do token.

## Cenários

1. Clientes sem Identificação
    1. Cria Conta em Anônimo

2. Cliente com Identificação
    1. Cria Conta com Identificação

3. Jornada do Cliente
    1. Cria Order
    2. Adiciona Produtos ao Pedido
    3. Faz Pagamento (Fake Checkout)

4. Jornada da Lanchonete
    1. Lista Pedidos que Tiveram Sucesso no Fake Checkout 
    2. Recebe Pedido com Status Aberto
    3. Possibilidade de Filtrar por Categoria
    4. Atualiza Status para Finalizado

5. Fluxo de Cadastro de Produto
    2. Criar
    3. Editar
    4. Excluir