# Continuous integration and continuous delivery

---

Nesta quarta entrega, apresentamos os processos para a implementação do Tech Challenge, cujo objetivo é desenvolver uma plataforma de vendas para uma lanchonete de bairro em plena expansão. Este documento detalha os testes unitários, cobertura de código e o fluxo de deploy baseado na branch principal. A implementação foi realizada utilizando o mesmo ambiente configurado na [fase 3](https://software-architecture-fiap.github.io/tech-challenge/fase_3/eks_infra_cicd/), garantindo consistência e continuidade. Para mais detalhes, consulte os manifestos do Terraform disponíveis no repositório [infra-kitchen](https://github.com/software-architecture-fiap/infra-kitchen).
 

---

## :material-wrench-outline: Checks de PR


## :material-wrench-outline: Cobertura de código


## :material-wrench-outline: Pipeline de Deploy


O deploy é acionado via comentário no PR (/deploy). O GitHub Actions executa as seguintes etapas:

- Build da imagem Docker com a tag baseada no commit SHA.
- Push da imagem para o Amazon ECR.
- Atualização do Kustomize para utilizar a nova imagem.
- Aplicar as configurações no cluster Kubernetes.

Fluxo de Nomenclatura e Deploy

Ambiente de Desenvolvimento: Deploy acionado com `/deploy` em um PR.

Ambiente de Produção: Baseado no versionamento semântico e nas seguintes regras de nome de branch:
- bugfix/ → Patch version
- feature/ → Minor version
- release/ → Major version
- doc/ ou misc/ → Apenas incrementação de build

