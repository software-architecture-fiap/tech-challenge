# Preparando Ambiente

Este projeto é um sistema de pedidos de lanches adaptável para web e mobile, focado no backend. A aplicação é
desenvolvida utilizando FastAPI, SQLAlchemy, e Docker.

## :octicons-package-dependencies-16: Pré-Requisitos
> Nota: Essa é uma etapa indispensável para habilitar o ambiente de avaliação do tech challenge!

1. **Sistema Operacional**: O projeto pode ser executado em qualquer sistema operacional que suporte Docker e Python.
Recomenda-se um sistema baseado em Unix (Linux ou macOS) para facilitar o uso de Docker;
2. **Python**: Versão 3.8 ou Superior;
3. **Docker**: Para Containerização da Aplicação.
4. **Docker Compose**: Para Orquestração dos Contêineres Docker.

## :simple-editorconfig: Configuração do Ambiente

### :simple-python: Instalação do Python

**:simple-linux: Linux  :simple-apple: macOS**:

```sh
sudo apt update
sudo apt install python3 python3-pip
```

**:fontawesome-brands-windows: Windows**:

- Baixe e instale o Python no [Site Oficial](https://www.python.org/downloads/).

### :simple-docker: Instalação do Docker

Siga as instruções no site oficial do Docker para instalar o Docker e Docker Compose:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### :simple-git: Clonando o Repositório

Clone este repositório para sua máquina local:
> Nota: Essa é uma etapa indispensável para habilitar o ambiente de avaliação do tech challenge!


```sh
git clone https://github.com/seu-usuario/tech-challenge.git
cd tech-challenge
```

### :material-database-check: Banco de Dados 
> Nota: Essa é uma etapa indispensável para habilitar o ambiente de avaliação do tech challenge!

- Crie um arquivo `.env` na raiz do projeto e defina as seguintes variáveis:

```bash
DATABASE_URL=postgresql://postgres:localhost%401988@db:5432/challenge
SECRET_KEY=mySecurePassword
ADMIN_NAME=Admin User
ADMIN_EMAIL=email@email.com.br
ADMIN_CPF=00000000000
ADMIN_PASSWORD=your_password

```

### :octicons-terminal-16: Instalando Dependências
> Nota: Essa é uma etapa indispensável para habilitar o ambiente de avaliação do tech challenge!

- Crie e ative um ambiente virtual (opcional, mas recomendado):

```sh
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

- Instale as Dependências do Projeto:

```sh
poetry install
```

- Execute as migrações do Alembic para criar o banco de dados e as tabelas necessárias:
> Nota: Etapa opcional para habilitar o ambiente de avaliação do tech challenge

    ```sh
    alembic revision --autogenerate -m 'initial migration'
    alembic upgrade head
    ```

### :material-infinity: Executando a Aplicação
> Nota: Essa é uma etapa indispensável para habilitar o ambiente de avaliação do tech challenge!

**Com Docker:**

Certifique-se de que o Docker e o Docker Compose estão instalados.
Navegue até a pasta do projeto e execute:

```sh
docker-compose up --build
```

A aplicação estará disponível em `localhost:2000`.

**Sem Docker:**
> Nota: Etapa opcional para habilitar o ambiente de avaliação do tech challenge

Execute o servidor FastAPI:

```sh
uvicorn app.main:app --host 0.0.0.0 --port 2000 --reload
```

A aplicação estará disponível em `localhost:2000`.

### :simple-swagger: Documentação da API

A documentação interativa da API está disponível em `localhost:2000/docs`.

### :material-folder: Estrutura de Arquivos

- `app/main.py`: Ponto de entrada da aplicação.
- `app/models.py`: Definição dos modelos de dados.
- `app/schemas.py`: Definição dos esquemas Pydantic para validação.
- `app/crud.py`: Funções CRUD para manipulação dos dados.
- `app/database.py`: Configuração do banco de dados e sessão.
- `app/routers`: Roteadores FastAPI para diferentes endpoints (clientes, produtos, pedidos).
- `app/middleware.py`: Middleware para limitação de taxa (Rate Limiting).

### :material-car-speed-limiter: Limitação de Taxa

Foi criado mas ainda não implementado um middleware para limitar as solicitações de um mesmo IP para o endpoint de
token. Este middleware usa Redis para rastrear e limitar as solicitações:

- Limite de 10 solicitações por minuto por IP.
- Mensagem de erro personalizada quando o limite é atingido.

### :material-open-source-initiative: Contribuição

Para contribuir com este projeto, siga os passos:

- Fork o repositório;
- Crie uma nova branch (`git checkout -b feature/nova-funcionalidade`);
- Commit suas mudanças (`git commit -am 'Adicionei uma nova funcionalidade'`);
- Push para a branch (`git push origin feature/nova-funcionalidade`);
- Abra um Pull Request;
