### **Subindo a Aplicação com Serverless Framework**

Este tutorial explica como fazer o **deploy** de uma aplicação com **Serverless Framework** já criada. Vamos configurar o ambiente, personalizar o arquivo `serverless.yml` e usar os comandos necessários para subir a aplicação para a AWS.

---

#### **Pré-requisitos**

Antes de começar, você precisa ter os seguintes pré-requisitos configurados:

- **AWS CLI** configurada com credenciais (acesso à AWS):
  ```bash
  aws configure
  ```
  Forneça sua **AWS Access Key**, **Secret Key**, região (ex.: `us-east-1`) e formato de saída (ex.: `json`).

- **Node.js** e **Serverless Framework** instalados globalmente:
  ```bash
  npm install -g serverless
  ```
  
---

#### **Passos para Subir a Aplicação com Serverless**

1. **Acessando o diretório da aplicação**

   Entre no diretório onde a aplicação já foi criada com o Serverless Framework.

   ```bash
   cd /.../auth-coffee
   ```

2. **Configurando o arquivo `serverless.yml`**

   O arquivo **`serverless.yml`** é o arquivo principal de configuração onde você define as funções Lambda, os recursos da AWS e eventos que disparam as funções.

   ```yaml
   service: tech-challenge
   
   frameworkVersion: '3'
   
   provider:
     name: aws
     region: sa-east-1
     ecr:
       images:
         tech-challenge:
           path: .
    .
    .
    .
   
   functions:
     api:
       image:
         name: tech-challenge
       events:
         - httpApi:
             path: /{proxy+} #Rota genérica, pois fará o redirecionamento para o Framework FastAPI via Magnum
             method: ANY
   
   plugins:
   - serverless-dotenv-plugin
   ```

   **Explicação:**
   - **service:** Nome do serviço ou aplicação.
   - **provider:** Definições do provedor de nuvem (AWS, no caso).
   - **functions:** Define as funções Lambda que serão implementadas.
   - **events:** O evento que aciona a função Lambda, no caso, uma requisição HTTP do API Gateway.
   - **plugins:** Caso você tenha dependências específicas, como em projetos Python.

3. **Verificando o `handler`**

   O **handler** é o arquivo onde a função Lambda é implementada.

   ```python
   handler = Mangum(
     app,
     lifespan="off",
     api_gateway_base_path=''
     )
   ```

4. **Instalar dependências (se houver)**

   Caso você tenha dependências para o seu projeto (ex.: com `pip` no Python ou `npm` no Node.js), instale-as:

   - Execute o arquivo `requirements.txt` com pip e instale as dependencias do projeto localmente:
     ```bash
     pip install -r requirements.txt
     ```

5. **Deploy da aplicação**

   Agora, com tudo configurado, basta rodar o comando para fazer o **deploy** da sua aplicação para a AWS:

   ```bash
   sls deploy
   ```

   Esse comando cria e configura os recursos necessários no AWS, como a função Lambda, API Gateway, e outros serviços que você definiu.

   **Saída esperada:**

   Após o deploy ser concluído, você verá um resultado semelhante a este:

   ```
   Deploying tech-challenge to stage dev (sa-east-1)
   
   ✔ Service deployed to stack tech-challenge-dev (646s)
   
   endpoint: ANY - https://xxxxx.execute-api.sa-east-1.amazonaws.com/{proxy+}                                                                                                                                                     
   functions:
     api: tech-challenge-dev-api                                                                                                                                                                                                       
   
   Monitor all your API routes with Serverless Console: run "serverless --console" 
   ```

   O link da API gerado será exibido na saída, e você poderá acessar o endpoint da sua função Lambda através do navegador ou ferramentas como **Postman**.

---

#### **Comandos Importantes do Serverless Framework**

- **Deploy da aplicação:**
  ```bash
  sls deploy
  ```

- **Visualizar as funções implantadas e recursos:**
  ```bash
  sls info
  ```

- **Remover a aplicação da AWS (excluir todos os recursos):**
  ```bash
  sls remove
  ```

- **Ver logs das funções Lambda:**
  ```bash
  sls logs -f hello
  ```

- **Invocar a função Lambda diretamente:**
  ```bash
  sls invoke -f hello
  ```

- **Testar localmente (para funções HTTP, por exemplo):**
  ```bash
  sls offline start
  ```