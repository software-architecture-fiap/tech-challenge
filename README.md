# Challenge 1

Este projeto é um sistema de pedidos de lanches adaptável para web e mobile, focado no backend. A aplicação é desenvolvida utilizando FastAPI, SQLAlchemy, e Docker.

## Pré-requisitos

1. **Sistema Operacional**: O projeto pode ser executado em qualquer sistema operacional que suporte Docker e Python. Recomenda-se um sistema baseado em Unix (Linux ou macOS) para facilitar o uso de Docker.
2. **Python**: Versão 3.8 ou superior.
3. **Docker**: Para containerização da aplicação.
4. **Docker Compose**: Para orquestração dos contêineres Docker.

## Configuração do Ambiente

### Instalação do Python

**Linux/macOS**:

```sh
sudo apt update
sudo apt install python3 python3-pip
```

**Windows**:

- Baixe e instale o Python no [site oficial](https://www.python.org/downloads/).

### Instalação do Docker

Siga as instruções no site oficial do Docker para instalar o Docker e Docker Compose:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Clonando o Repositório

Clone este repositório para sua máquina local:

```sh
git clone https://github.com/seu-usuario/tech-challenge.git
cd tech-challenge
```

### Configuração do Banco de Dados

1. **Criar Banco de Dados e Usuário no PostgreSQL**:

- Acesse o PostgreSQL (certifique-se de que o serviço está em execução).

```sh
sudo -u postgres psql
```

- Execute os comandos SQL para criar o banco de dados e o usuário:

```sql
CREATE DATABASE mydb;
\c mydb
CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```

- Crie um arquivo `.env` na raiz do projeto e defina as seguintes variáveis:

```bash
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydb
SECRET_KEY=mySecurePassword
```

### Instalando Dependências

- Crie e ative um ambiente virtual (opcional, mas recomendado):

```sh
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

- Instale as dependências do projeto:

```sh
pip install -r requirements.txt
```

### Executando a Aplicação

**Com Docker:**

Certifique-se de que o Docker e o Docker Compose estão instalados.
Navegue até a pasta do projeto e execute:

```sh
docker-compose up --build
```

A aplicação estará disponível em `localhost:2000`.

**Sem Docker:**

Execute o servidor FastAPI:

```sh
uvicorn app.main:app --host 0.0.0.0 --port 2000
```

A aplicação estará disponível em `localhost:2000`.

### Documentação da API

A documentação interativa da API está disponível em `localhost:2000/docs`.

### Estrutura de Arquivos e Funções

- `app/main.py`: Ponto de entrada da aplicação.
- `app/models.py`: Definição dos modelos de dados.
- `app/schemas.py`: Definição dos esquemas Pydantic para validação.
- `app/crud.py`: Funções CRUD para manipulação dos dados.
- `app/database.py`: Configuração do banco de dados e sessão.
- `app/routers`: Roteadores FastAPI para diferentes endpoints (clientes, produtos, pedidos).
- `app/middleware.py`: Middleware para limitação de taxa (Rate Limiting).

### Limitação de Taxa

Foi criado mas ainda não implementado um middleware para limitar as solicitações de um mesmo IP para o endpoint de token. Este middleware usa Redis para rastrear e limitar as solicitações:

- Limite de 3 solicitações por minuto por IP.
- Mensagem de erro personalizada quando o limite é atingido.

### Contribuição

Para contribuir com este projeto, siga os passos:

- Fork o repositório.
- Crie uma nova branch (`git checkout -b feature/nova-funcionalidade`).
- Commit suas mudanças (`git commit -am 'Adicionei uma nova funcionalidade'`).
- Push para a branch (`git push origin feature/nova-funcionalidade`).
- Abra um Pull Request.
