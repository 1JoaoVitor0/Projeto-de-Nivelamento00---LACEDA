# Desafio de Nivelamento LACEDA 2026 - RH Analytics

Projeto desenvolvido como parte do processo de nivelamento da **LACEDA (Liga Acadêmica de Engenharia e Ciência de Dados)**, com foco na aplicação de conceitos de Engenharia e Ciência de Dados em um cenário real de análise de Recursos Humanos.

---

## Objetivo

Atuando como **Engenheiro de Dados**, este projeto tem como objetivo processar, higienizar e analisar os dados do departamento de Recursos Humanos de um escritório de advocacia para identificar os principais fatores que contribuem para a evasão (**turnover**) dos colaboradores.

---

## Stack Tecnológica

- **Gerenciamento de ambiente:** `uv`
- **Linguagem:** Python 3.11
- **Processamento de dados:** Pandas

### Visualização de Dados e Dashboard

- Streamlit
- Jupyter Notebook

---

## 📂 Estrutura do Repositório

```text
.
├── data
│   ├── raw/          # Dados originais imutáveis fornecidos pela liga
│   └── processed/    # Tabela Base Analítica (ABT) consolidada e higienizada
│
├── notebooks/        # Análise Exploratória de Dados (EDA)
│
├── src/              # Scripts do pipeline ETL
│
└── README.md
```

---

## Decisões de Arquitetura e Engenharia de Dados

Durante a etapa de transformação (`src/transform.py`), foram adotadas as seguintes premissas para garantir consistência, rastreabilidade e qualidade dos dados.

### Padronização Financeira

A coluna `salario_base` foi tratada removendo a representação monetária (`R$`) e normalizando os separadores decimais. A conversão foi realizada de forma segura para o tipo `float`, evitando expressões regulares desnecessárias.

### Padronização de Datas

As datas apresentavam formatos mistos (ISO e brasileiro). Para evitar ambiguidades, a conversão utilizou:

```python
dayfirst=True
```

garantindo a interpretação correta dos registros.

### Integridade Referencial da Hierarquia

Os valores ausentes na coluna `id_reporta_a` foram identificados como colaboradores pertencentes ao nível de **Sócios**.

Para preservar a integridade referencial e manter a coluna como inteiro (`int`), foi utilizado o identificador fictício:

```text
-1
```

representando a ausência de superior hierárquico.

### Preservação de Dados de Negócio

Os valores ausentes nas colunas:

- `score_satisfacao`
- `data_promocao`

**não foram imputados** com médias, medianas ou valores padrão.

A análise exploratória demonstrou que a ausência desses registros representa um comportamento real do negócio (abstenção, falta de avaliação ou inexistência de promoção), e não um erro de coleta. A imputação desses valores introduziria viés nas análises e indicadores.

---

# Principais análises

## 1. A crise do burnout

O turnover não ocorre de forma homogênea.

Colaboradores do nível **Júnior** que foram desligados apresentaram, em média:

- **47 horas extras por mês**
- **56 processos sob responsabilidade**

Esses valores representam aproximadamente **três vezes** a média observada entre os demais colaboradores, indicando uma sobrecarga significativa na base operacional da empresa.

---

## 2. Foco de liderança

Ao cruzar os indicadores de satisfação com as taxas de turnover, foram identificados três gestores com desempenho significativamente inferior ao restante da organização:

- Gestor **ID 200**
- Gestor **ID 400**
- Gestor **ID 501**

Todos apresentam taxas de evasão superiores a **30%**, sugerindo necessidade de revisão das práticas de liderança e gestão de equipes.

---

## 🚀 Tecnologias Utilizadas

- Python 3.11
- Pandas
- uv
- Stremalit

---

## 👨‍💻 Autor

**Arthur Batista**

Projeto desenvolvido para o processo de nivelamento da **LACEDA (Liga Acadêmica de Engenharia e Ciência de Dados)**.