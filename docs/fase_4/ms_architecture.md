# Arquitetura de microsserviços

---

## :material-wrench-outline: Auth service

Esse microsserviço é responsável pela etapa de autenticação de clientes identificados, não identificados e usuários administrativos. Além disso, esse serviço também faz a geração de tokens JWT para autenticação em outro serviços. Contendo os endpoints para o gerenciamento de usuários.

### :material-dots-circle: Funcionalidades
- **Autenticação de usuários:** Geração de tokens JWT para autenticação.
- **Cadastro de usuários:** Permite que novos usuários se cadastrem no sistema.
- **Validação de tokens:** Valida se os tokens enviados em requisições são válidos.
- **Integração com outros** serviços: O Auth Service é consumido por outros serviços para validar a autenticidade de requisições.

### :material-code-json: Endpoints

- POST /token: Solicita um bearer token.
- GET /auth: Valida a autorização do bearer token.
- POST /customers/admin: Cria o usuário administrador da aplicação
- GET /customer/: Recupera a lista de usuários cadastrados.
- POST /customer/identify: Identifica um usuário pelo CPF.
- POST /customer/register: Criar o usuário identificado.
- POST /customer/anonymous: Criar o usuário anônimo.