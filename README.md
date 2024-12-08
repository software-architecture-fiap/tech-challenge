# Tech Challenge - SOAT 2024 - #25

Este projeto é um sistema de gerenciamento de pedidos desenvolvido para uma lanchonete em expansão. A solução de software é projetada para ser responsiva tanto em plataformas Web quanto Mobile. O backend, documentado e acessível via Swagger, permite uma administração eficiente e integrada dos pedidos, garantindo escalabilidade e facilidade de manutenção.

Você encontrará todos os passos do nosso projeto através deste link na nossa
[Plataforma de Documentação](https://software-architecture-fiap.github.io/tech-challenge/).

![Interrogate](docs/assets/interrogate_badge.svg)

## Desenvolvido com

- [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://docs.python.org/3/)
- [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
- [![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=Kubernetes&logoColor=white)](https://kubernetes.io/pt-br/docs/home/)
- [![Docker](https://img.shields.io/badge/docker-257bd6?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/)
- [![PostgresSQL](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
- [![Typed with: pydantic](https://img.shields.io/badge/typed%20with-pydantic-BA600F.svg?style=for-the-badge)](https://docs.pydantic.dev/)

---

### Contribuição

[![Open Issues](https://img.shields.io/github/issues-raw/software-architecture-fiap/tech-challenge?style=for-the-badge)](https://github.com/software-architecture-fiap/tech-challenge/issues)
[![Closed Issues](https://img.shields.io/github/issues-closed-raw/software-architecture-fiap/tech-challenge?style=for-the-badge)](https://github.com/software-architecture-fiap/tech-challenge/issues?q=is%3Aissue+is%3Aclosed)
[![Open Pulls](https://img.shields.io/github/issues-pr-raw/software-architecture-fiap/tech-challenge?style=for-the-badge)](https://github.com/software-architecture-fiap/tech-challenge/pulls)
[![Closed Pulls](https://img.shields.io/github/issues-pr-closed-raw/software-architecture-fiap/tech-challenge?style=for-the-badge)](https://github.com/software-architecture-fiap/tech-challenge/pulls?q=is%3Apr+is%3Aclosed)
[![Contributors](https://img.shields.io/github/contributors/software-architecture-fiap/tech-challenge?style=for-the-badge)](https://github.com/software-architecture-fiap/tech-challenge/contributors)
[![Activity](https://img.shields.io/github/last-commit/software-architecture-fiap/tech-challenge?style=for-the-badge&label=most%20recent%20activity)](https://github.com/software-architecture-fiap/tech-challenge/pulse)

---

# CI/CD using Github Actions

The pipeline [build-and-deploy](.github/workflows/build-and-deploy.yml) is designed to build and push container images to Amazon ECR and deploy them to an EKS cluster based on specific triggers.

### Repository Integration with AWS Credentials

> **Note:** This step is crucial to ensure a secure connection with AWS resources. Credentials are necessary for the pipeline to authenticate and interact with AWS ECR and EKS.

Update the repository settings under `Secrets and variables` > `Actions` with the following values:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`

## Workflow Triggers

The pipeline is triggered by the following events:

- **Issue Comment**: When a comment is created, edited, or deleted on an issue that contains `/deploy-dev`
- **Push**: When code is pushed to the `main` branch.

### Environment Variables

The following environment variables are defined for use throughout the pipeline:

- `AWS_REGION`: The AWS region where resources are located (`us-east-1`).
- `ECR_REPOSITORY`: The ECR repository name (`app/web`).
- `EKS_CLUSTER_NAME`: The EKS cluster name (`EKS-lanchonete-cluster`).

## Tasks

### Build and deploy

This job runs on `ubuntu-latest` and is executed if the event is an issue comment or a push to the `main` branch.

#### Steps

1. **Checkout Repository**

   - Uses the `actions/checkout@v4` action to checkout the repository.

2. **Check for Deploy-Dev Comment**

   - Checks if the event is an issue comment containing `/deploy-dev` and prints a message if true.

3. **Versioning Image**

   - Determines the image tag based on the event type:
     - Production: using `push` events to the `main` branch, increments the semantic version, considering the main branch as production.
     - Development: it is trigger using the commit SHA with a `-dev` suffix.

4. **Configure AWS Credentials**

   - Uses the `aws-actions/configure-aws-credentials@v1` action to configure AWS credentials using secrets.

5. **Login to ECR Registry**

   - Uses the `aws-actions/amazon-ecr-login@v1` action to log in to the ECR registry.

6. **Build and Push the Container Image**

   - Builds and pushes the container image to the ECR repository using tag.

7. **Commit and Push Updated Version**

   - Commits and pushes the updated version file if the event is a push to the `main` branch.

8. **Setup Kubeconfig**

   - Sets up the kubeconfig for the EKS cluster using AWS CLI.

9. **Deploy Application to Kubernetes Cluster**
   - Deploys the application to the Kubernetes cluster in the `development` namespace if the event is an issue comment containing `/deploy-dev`.
   - Deploys the application to the `production` namespace on the EKS cluster when a commit is pushed to the `main` branch after merging a pull request.

## Deployment Logic

The deployment logic varies based on the environment:

- **Development Environment**: Triggered by issue comments containing `/deploy-dev`.
- **Production Environment**: Triggered by pushes to the `main` branch.

The deployment process includes:

- Setting the environment and kustomize directory.
- Checking and creating the namespace if it doesn't exist.
- Updating the image in the kustomize configuration.
- Applying the Kubernetes resources using `kubectl`.
