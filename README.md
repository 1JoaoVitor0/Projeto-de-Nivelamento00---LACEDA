# Análise de evasão de colaboradores — Arquitetura Medalhão

Projeto de Engenharia e Análise de Dados para investigar fatores associados ao desligamento de colaboradores. A solução separa dados brutos, dados confiáveis e dados analíticos, o que permite reprocessamento e rastreabilidade.

## Arquitetura

```text
dados/ (fonte imutável) → data/bronze/ → data/silver/ → data/gold/ → notebooks/
                              cópia        limpeza       métricas      análise
```

- **Bronze:** cópia fiel dos CSVs de origem.
- **Silver:** tabelas tipadas, padronizadas e validadas em Parquet.
- **Gold:** visão única `evasao_colaboradores.parquet`, enriquecida com departamento, filial e indicadores analíticos.

Os artefatos gerados em `data/` e o relatório de execução são ignorados pelo Git, pois são reproduzíveis pelo pipeline. A pasta `dados/` é a entrada original e não deve ser alterada.

## Como executar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/run_pipeline.py
jupyter lab notebooks/analise_evasao.ipynb
```

## Tratamentos aplicados

- remove duplicidades integrais e IDs repetidos de forma determinística;
- remove números indevidos dos nomes, ajusta espaçamento e capitalização;
- padroniza `Fem` para `Feminino`, datas ISO e `dd/mm/aaaa`, moeda brasileira e booleanos; também corrige o nome técnico `processos_actifs` para `processos_ativos` a partir da Silver;
- marca a ausência de satisfação em `score_satisfacao_ausente` e imputa a mediana por nível, preservando o sinal de imputação;
- mantém `data_promocao` nula quando não houve promoção, pois é ausência de negócio esperada;
- valida faixas de salário, bônus, satisfação, processos e horas extras; valores inválidos são nulos;
- valida chaves de departamento e filial antes de produzir Gold.

O relatório `reports/data_quality_report.json` registra as métricas de qualidade de cada execução. Os scripts também podem ser executados separadamente: `python src/bronze.py`, `python src/silver.py` e `python src/gold.py`, nessa ordem.

## Indicadores da camada Gold

Além dos atributos originais, a camada Gold inclui `desligado_flag`, tempo de casa, promoção, remuneração estimada com bônus e faixas para satisfação, horas extras e tempo de casa. A data de referência é fixa (`2026-01-01`) para que o resultado seja reproduzível.


