# Infra-Kitchen


Nesta etapa apresentamos os processos e práticas adotados para o gerenciamento da infraestrutura utilizada no Tech Challenge 3. 
Contendo os detalhes para configurar, provisionar e gerenciar o Kubernetes no EKS, bem como as boas práticas para garantir um processo seguro e eficiente. 
O repositório que contém os manifestor do Terraform o [infra-kitchen](https://github.com/software-architecture-fiap/infra-kitchen).

---

## :material-wrench-outline: Requisitos e configuração do ambiente

A infraestrutura utiliza uma conta AWS Academy, que possui limitações de recursos e sessões com duração de 4 horas. 
É essencial seguir rigorosamente os passos abaixo para evitar atrasos ou inconsistências no provisionamento:

1. **Configuração de credenciais:**
    - Inicie o laboratório na AWS Academy.
    - Acesse o botão **AWS Details** e, em seguida, clique em **AWS CLI** para visualizar as credenciais temporárias.
    - Copie e cole o conteúdo exibido diretamente no arquivo `~/.aws/credentials` no terminal.

2. **Configuração no HCP:**
    - Atualize os valores das credenciais AWS nas configurações do HCP: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e `AWS_SESSION_TOKEN`.
    - Navegue para `Settings > Variable Set` nos [workspaces HCP infra-kitchen](https://app.terraform.io/app/tc_fiap/workspaces) e insira as variáveis mencionadas.

3. **Ferramentas necessárias:**
    - Certifique-se de ter o Terraform instalado localmente.
    - Utilize as versões recomendadas no guia do Tech Challenge.

---

## :material-console-line: Validação local

Para garantir a integridade do código e identificar problemas antes de um deploy, utilize os comandos a seguir:

- **`terraform init`**: Inicializa o diretório local e prepara os plugins necessários.
- **`terraform fmt`**: Corrige a formatação dos arquivos `.tf`.
- **`terraform validate`**: Verifica se as configurações são válidas e consistentes.
- **`terraform plan`**: Gera um plano de execução para prever alterações na infraestrutura.

---

## :material-link: Integração com o HCP

### :material-information-outline: Visão geral
Utilizamos o [HCP Terraform](https://developer.hashicorp.com/terraform/cloud-docs) para centralizar e padronizar o gerenciamento da infraestrutura. 
Este ambiente permite:

- Execuções consistentes do Terraform.
- Colaboração simplificada, com histórico compartilhado de alterações.
- Controle de acesso individualizado para membros da equipe.

### :material-timeline: Fluxo de trabalho

#### :material-robot-outline: Fluxo automático

1. **Execução automática do `terraform plan`:**
    - A cada push, um plano de execução é gerado para prever mudanças.
    - Após o merge de um PR, um novo `terraform plan` e um `terraform apply` são executados automaticamente.

2. **Monitoramento no HCP:**
    - Acompanhe os logs detalhados e status de execução através dos [runs do HCP](https://app.terraform.io/app/tc_fiap/workspaces/infra-kitchen/runs).

#### :material-hand-wrench: Etapas manuais

Em casos de erro, intervenções manuais podem ser necessárias. Certifique-se de registrar qualquer ajuste manual no log ou em uma issue do repositório desse projeto.

---

## :material-rocket-launch: Tutorial: Provisionando a infra no EKS

1. **Criar e executar merge de um pull request:**
    - Atualize os valores no HCP e no ambiente local.
    - Submeta um PR no repositório e realize o merge na branch principal. 
    - A execução automática do `terraform plan` e `terraform apply` será iniciada.

2. **Obter o Kubeconfig:**
    - Após a infraestrutura estar ativa, utilize os comandos abaixo para configurar o acesso ao cluster Kubernetes:

```bash
    aws eks --region us-east-1 update-kubeconfig --name EKS-lanchonete-cluster

    kubectl cluster-info
    ❯ kubectl cluster-info
    Kubernetes control plane is running at https://8A378062CC9AEEE22CD23D0F97BDBAF3.gr7.us-east-1.eks.amazonaws.com
    CoreDNS is running at https://8A378062CC9AEEE22CD23D0F97BDBAF3.gr7.us-east-1.eks.amazonaws.com/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

    To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

3. **Deploy de manifestos no Kubernetes:**
    - Navegue até o repositório do app service.
    - Configure o diretório de manifests com o comando:
    - 
```bash
      KUSTOMIZE_DIR="$(pwd)/infra/kubernetes/development"
      kubectl apply -k $KUSTOMIZE_DIR -n development
      kubectl get pod -n development
```
---

## :material-alert-decagram-outline: Fluxos de destroy

Para evitar exclusões acidentais, os processos de destruição são restritos às configurações do HCP. Siga os passos abaixo:

1. **Acesse o workspace:**
   - Entre no HCP infra-kitchen workspace.
2. **Acione o destroy:**
   - Navegue para a aba Settings e selecione Destruction and Deletion.
   - Programe ou inicie manualmente a destruição da infraestrutura.

---

## :material-file-tree-outline: Regras do repositório

- Boas práticas de versionamento:
  - Utilize mensagens de commit claras e padronizadas.
  - Realize revisões de PR com foco em consistência e segurança.

---

## :material-check-decagram: Integração contínua
### :material-code-tags-check: Verificações automáticas com TFLint

O repositório que provisiona a infra no EKS repositório possui verificações automáticas via GitHub Actions para garantir a qualidade do código IaC. 
A cada commit, as seguintes ações são executadas:

- Formatação do Código: verificação de padrões estabelecidos para arquivos Terraform.
- Validação Sintática: garantia de que as configurações não contenham erros estruturais.

Certifique-se de revisar os relatórios gerados no plan/apply e tente corrigir quaisquer problemas antes de enviar novas alterações.
