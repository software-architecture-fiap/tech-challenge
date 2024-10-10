# Clean Code
## Manutenção de Código Limpo

Para assegurar que nosso código permaneça limpo, legível e fácil de manter, implementamos diversas automatizações e ferramentas de linting. Essas medidas minimizam o esforço necessário para manter a estrutura do projeto organizada. A seguir, detalhamos as ações que tomamos para alcançar esse objetivo.

### Ferramentas de Linting e Formatação

#### :simple-ruff: Ruff
O `Ruff` é uma ferramenta de linting e formatação para Python que integra diversas funcionalidades de análise estática de código em um único pacote. Ele verifica o código em busca de padrões que possam ser otimizados, erros comuns, violações de estilo (como o PEP 8) e realiza sugestões de melhorias. Além disso, o Ruff formata o código automaticamente, ajustando espaçamento, indentação e garantindo consistência no estilo de acordo com as regras configuradas. Por ser altamente eficiente e rápido, ele é indicado para grandes projetos que requerem verificação e correção de estilo de forma ágil.

#### :simple-sonarlint: Sonar Lint
Além das configurações e bibliotecas automatizadas, utilizamos o plugin SonarLint para realizar verificações e fornecer sugestões em nosso código. Isso nos ajuda a refletir sobre nosso projeto durante o desenvolvimento, garantindo a qualidade e a conformidade com as melhores práticas.

#### :material-source-repository-multiple: Sourcery
Assim como o SonarLint, o Sourcery verifica nosso código em nível de repositório. Ele funciona como uma análise profunda do projeto, identificando áreas que podem ser otimizadas e sugerindo melhorias para aumentar a eficiência e a qualidade do código.

### Automação de Verificações

#### :simple-precommit: Pre-Commit
`Pre-Commit` é uma ferramenta que automatiza a execução de verificações de qualidade no código antes de cada commit. Ela permite configurar uma série de hooks (verificações) que são executados automaticamente, como linters, formatação de código, verificação de erros ou testes de segurança. Esses hooks no nosso projeto incluem o Ruff. Isso ajuda a garantir que o código siga as melhores práticas, mantendo a consistência e evitando que erros cheguem ao repositório. Sempre que fazemos um commit, o Pre-Commit impede que prossigamos se algo estiver fora do padrão.

#### :simple-githubactions: Github Actions
Adicionamos validações pós-commit com o GitHub Actions para garantir a qualidade do código durante o push. Isso proporcionará uma camada adicional de segurança em relação à qualidade do código. Caso seja desabilitado o `Pre-commit` em sua IDE, o workflow do GitHub Actions identificará o problema com nossas ações configuradas.

### Testes e Cobertura

#### :material-test-tube: Testes Unitários
Implementamos uma estrutura para que os testes unitários sejam executados após cada commit. Além disso, utilizamos o conceito de testes locais para facilitar o desenvolvimento, permitindo que os desenvolvedores verifiquem a funcionalidade do código antes de enviá-lo para o repositório.

#### :material-view-list: Pytest Coverage
Pytest Coverage é uma extensão do framework de testes `pytest` que mede a cobertura de testes no código Python. Ele gera relatórios detalhados sobre quais partes do código foram executadas durante a execução dos testes e quais não foram, ajudando a identificar áreas não testadas. A cobertura é essencial para garantir que os testes validem o máximo possível do comportamento do código, aumentando sua confiabilidade.

### Documentação

#### :simple-googledocs: Docstrings
Docstrings são strings de documentação usadas para descrever o propósito, funcionamento e detalhes de uma função, classe, método ou módulo em Python. Elas são colocadas logo abaixo da definição do elemento e seguem o padrão de boas práticas recomendado pela PEP 257. Docstrings facilitam a compreensão do código, ajudam a gerar documentação automaticamente e são acessíveis via `help()`. O formato pode variar (Google, NumPy, Sphinx), mas deve incluir a descrição geral, parâmetros, valor de retorno e exceções, quando aplicável. Exemplo no formato Google:

```python
def soma(a: int, b: int) -> int:
    """
    Soma dois números inteiros.

    Args:
        a (int): O primeiro número.
        b (int): O segundo número.

    Returns:
        int: A soma dos dois números.
    """
    return a + b
```
Essas docstrings descrevem claramente a função e seus componentes, facilitando a compreensão e manutenção do código.

#### :material-view-list: Interrogate
Interrogate é uma ferramenta de análise estática para Python que verifica se o código está adequadamente documentado com docstrings. Ele percorre o código-fonte e gera relatórios indicando quais funções, classes e métodos estão sem docstrings, auxiliando na conformidade com padrões de documentação, como o PEP 257. O Interrogate também permite configurar a cobertura mínima de docstrings que um projeto deve ter e pode ser integrado com ferramentas como Pre-Commit para garantir que todo o novo código atenda aos requisitos de documentação.

### Gerenciamento de Dependências e Tarefas

#### :simple-poetry: Poetry
Agora, temos total controle sobre o escopo do projeto ao adicionar um gerenciador de dependências mais robusto do que um simples arquivo `requirements.txt`. Isso nos proporciona segurança quanto à compatibilidade entre as dependências e reduz o risco de conflitos de versão.

#### :material-robot: Taskipy
O `Taskipy` facilita a criação e o uso de atalhos para a linha de comando, similar a um Makefile ou aliases. Com ele, podemos definir diversos comandos no arquivo `pyproject.toml`, simplificando a execução de tarefas comuns. Por exemplo, em vez de lembrar uma série de comandos complexos, podemos simplesmente executar `task test` para rodar os testes.

### Tipagem

#### :material-view-list: Type Hints
Type Hints em Python são anotações opcionais usadas para indicar os tipos de variáveis, parâmetros e valores de retorno em funções. Elas melhoram a legibilidade do código, facilitam a manutenção e permitem a detecção antecipada de erros por ferramentas de análise estática, como linters e IDEs. Embora não alterem o comportamento do código em tempo de execução, os Type Hints ajudam os desenvolvedores a entender melhor as expectativas de tipos, tornando o código mais robusto e confiável. Exemplo:

```python
def soma(a: int, b: int) -> int:
    return a + b
```

Neste exemplo, a função `soma` espera dois parâmetros do tipo inteiro e retorna um valor inteiro.
