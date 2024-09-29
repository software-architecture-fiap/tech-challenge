# Clean Code

Para garantir que sempre teremos um Código Limpo que seja fácil de ser lido e mantido, fizemos uma série de
automatizações e inclusões de mecanismos e lints para que o trabalho de manter a estrutura organizada seja mínimo.
Iremos descrever abaixo todas as medidas que tomamos para tornar isso possível.

## :simple-ruff: Ruff

O Ruff é uma ferramenta de formatação e linting para Python que combina diversas funcionalidades de análise
estática de código em um único pacote. Ele verifica o código em busca de padrões que possam ser otimizados,
erros comuns, violações de estilo (como o PEP 8), e realiza sugestões de melhorias. Além disso, o Ruff formata o
código automaticamente, ajustando espaçamento, indentação, e garantindo consistência no estilo de acordo com as
regras configuradas. Por ser altamente eficiente e rápido, ele é indicado para grandes projetos que requerem
verificação e correção de estilo de forma ágil.

## :simple-precommit: Pre-Commit

Pre-Commit é uma ferramenta que automatiza a execução de verificações de qualidade no código antes de cada commit.
Ela permite configurar uma série de hooks (verificações) que são executados automaticamente, como linters,
formatação de código, verificação de erros ou testes de segurança. Esses hooks no nosso projeto incluem o Ruff. 
Isso ajuda a garantir que o código siga as melhores práticas, mantendo a consistência e evitando que erros cheguem 
ao repositório. Sempre que fazemos um Commit, o Pre-Commit impede que prossigamos se algo estiver fora do padrão.

## :simple-githubactions: Github Actions

Adicionamos validações Post-Commit com o Github Actions validando a qualidade do código em tempo de push. Isso
nos dá mais uma camada de segurança quanto à qualidade do código. Caso alguém tente desabilitar o Pre-Commit
em sua IDE, o Workflow do Github Actions irá acusar com nossas Actions configuradas.

## :material-test-tube: Testes Unitários

Implementamos uma estrutura para que os testes unitários sejam efetuados em Post-Commit. Além de termos usado o
conceito de testes locais para facilitar o desenvolvimento.

## :simple-poetry: Poetry

Agora, temos total controle sobre o escopo do projeto ao adicionar um gerenciador de dependências mais robusto
que um simples arquivo requirements.txt. Temos segurança sobre a compatibilidade entre as dependências.

## :material-robot: Taskipy

Assim como um Makefile ou uma espécie de Alias, o Taskipy consegue democratizar o uso de atalhos para a linha de
comando. Podemos criar vários atalhos de combinações de atalhos dentro do pyproject.toml usando essa ferramenta.
Com isso, não precisamos decorar uma série de atalhos, basta chamar um task test, por exemplo.

## :material-view-list: Type Hints

Type Hints em Python são anotações opcionais usadas para indicar os tipos de variáveis, parâmetros e valores de
retorno em funções. Elas melhoram a legibilidade do código, facilitam a manutenção e permitem a detecção antecipada
de erros por ferramentas de análise estática, como linters e IDEs. Embora não alterem o comportamento do código em
tempo de execução, os Type Hints ajudam desenvolvedores a entender melhor as expectativas de tipos, tornando o
código mais robusto e confiável. Exemplo:

```python
def soma(a: int, b: int) -> int:
    return a + b
```

Aqui, a função soma espera dois inteiros e retorna um inteiro.

## :simple-googledocs: Docstrings

Docstrings são strings de documentação usadas para descrever o propósito, funcionamento e detalhes de uma função,
classe, método ou módulo em Python. Elas são colocadas logo abaixo da definição do elemento e seguem o padrão de
boas práticas recomendado pela PEP 257. Docstrings facilitam a compreensão do código, ajudam a gerar documentação
automaticamente e são acessíveis via help(). O formato pode variar (Google, NumPy, Sphinx), mas deve incluir a
descrição geral, parâmetros, valor de retorno e exceções, quando aplicável. Exemplo no formato Google:

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
Essas docstrings ajudam a descrever a função e seus componentes de maneira clara.

## :material-view-list: Interrogate

Interrogate é uma ferramenta de análise estática para Python que verifica se o código está adequadamente
documentado com docstrings. Ele percorre o código-fonte e gera relatórios indicando quais funções, classes e
métodos estão faltando docstrings, auxiliando na garantia de conformidade com padrões de documentação, como o
PEP 257. O Interrogate também permite configurar a cobertura mínima de docstrings que um projeto deve ter, e pode
ser integrado com ferramentas como pre-commit para garantir que todo o novo código atenda aos requisitos de
documentação.

## :material-view-list: Pytest Coverage

Pytest Coverage é uma extensão do framework de testes pytest que mede a cobertura de testes no código Python.
Ele gera relatórios detalhados sobre quais partes do código foram executadas durante a execução dos testes e quais
não foram, ajudando a identificar áreas não testadas. A cobertura é importante para garantir que os testes validem
o máximo possível do comportamento do código, aumentando sua confiabilidade.

## :simple-sonarlint: Sonar Lint

Além das configurações e bibliotecas automatizadas, usamos o plugin do Sonar Lint para fazer checagens e dicas
em nosso código. Isso nos ajuda a refletir sobre nosso projeto em tempo de desenvolvimento.

## :material-source-repository-multiple: Sourcery

Assim como o Sonar Lint, o Sourcery para verificar nosso código em nível de repositório. Então ele funciona como
uma ultrassonografia do projeto.
