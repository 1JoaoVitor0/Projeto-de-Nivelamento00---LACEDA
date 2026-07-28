import json
from datetime import date

import pandas as pd

from config import BRONZE_DIR, REPORT_DIR, SILVER_DIR
from utils import parse_currency, parse_date, read_csv


def clean_dimensions(departments: pd.DataFrame, branches: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    departments = departments.drop_duplicates(subset="id_departamento", keep="first").copy()
    branches = branches.drop_duplicates(subset="id_filial", keep="first").copy()
    departments["nome_departamento"] = departments["nome_departamento"].str.replace(r"\s+", " ", regex=True).str.title()
    branches["cidade"] = branches["cidade"].str.replace(r"\s+", " ", regex=True).str.title()
    branches["estado"] = branches["estado"].str.upper()
    return departments, branches


def clean_employees(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    metrics: dict[str, int] = {"linhas_entrada": len(frame)}
    frame = frame.rename(columns={"processos_actifs": "processos_ativos"})
    metrics["duplicados_exatos_removidos"] = int(frame.duplicated().sum())
    frame = frame.drop_duplicates().copy()
    duplicate_ids = frame.duplicated(subset="id_colaborador", keep="first")
    metrics["ids_duplicados_removidos"] = int(duplicate_ids.sum())
    frame = frame.loc[~duplicate_ids].copy()

    original_name = frame["nome"].copy()
    frame["nome"] = frame["nome"].astype("string").str.replace(r"\d+", "", regex=True).str.replace(r"\s+", " ", regex=True).str.strip().str.title()
    invalid_names = frame["nome"].isna() | ~frame["nome"].str.match(r"^[A-Za-zÀ-ÿ' -]{3,}$", na=False)
    metrics["nomes_padronizados"] = int((original_name != frame["nome"]).fillna(False).sum())
    metrics["nomes_invalidos"] = int(invalid_names.sum())
    frame.loc[invalid_names, "nome"] = "Nao informado"

    frame["genero"] = frame["genero"].replace({"Fem": "Feminino", "fem": "Feminino"})
    frame["nivel"] = frame["nivel"].replace({"Junior": "Júnior", "Senior": "Sênior"})
    frame["status_atual"] = frame["status_atual"].str.title()
    frame["home_office"] = frame["home_office"].astype("string").str.lower().map({"true": True, "false": False}).astype("boolean")
    frame["data_admissao"] = parse_date(frame["data_admissao"])
    frame["data_promocao"] = parse_date(frame["data_promocao"])
    frame["salario_base"] = parse_currency(frame["salario_base"])
    for col in ("id_colaborador", "id_departamento", "id_filial", "id_reporta_a", "processos_ativos", "horas_extras_mes", "percentual_bonus"):
        frame[col] = pd.to_numeric(frame[col], errors="coerce").astype("Int64")
    frame["score_satisfacao"] = pd.to_numeric(frame["score_satisfacao"], errors="coerce")
    frame["score_satisfacao_ausente"] = frame["score_satisfacao"].isna()
    score_by_level = frame.groupby("nivel")["score_satisfacao"].transform("median")
    frame["score_satisfacao"] = frame["score_satisfacao"].fillna(score_by_level).fillna(frame["score_satisfacao"].median())
    metrics["scores_imputados"] = int(frame["score_satisfacao_ausente"].sum())

    invalid_ranges = {
        "salario_base": frame["salario_base"].le(0),
        "percentual_bonus": ~frame["percentual_bonus"].between(0, 100),
        "score_satisfacao": ~frame["score_satisfacao"].between(1, 5),
        "horas_extras_mes": frame["horas_extras_mes"].lt(0),
        "processos_ativos": frame["processos_ativos"].lt(0),
    }
    for column, invalid in invalid_ranges.items():
        metrics[f"{column}_fora_da_faixa"] = int(invalid.fillna(True).sum())
        frame.loc[invalid, column] = pd.NA
    return frame, metrics


def run() -> None:
    employees = read_csv(BRONZE_DIR / "funcionarios.csv")
    departments = read_csv(BRONZE_DIR / "departamentos.csv")
    branches = read_csv(BRONZE_DIR / "filiais.csv")
    employees, metrics = clean_employees(employees)
    departments, branches = clean_dimensions(departments, branches)
    invalid_department = int((~employees["id_departamento"].isin(departments["id_departamento"])).sum())
    invalid_branch = int((~employees["id_filial"].isin(branches["id_filial"])).sum())
    if invalid_department or invalid_branch:
        raise ValueError(f"Chaves estrangeiras invalidas: departamento={invalid_department}, filial={invalid_branch}")
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    for name, table in {"funcionarios": employees, "departamentos": departments, "filiais": branches}.items():
        table.to_parquet(SILVER_DIR / f"{name}.parquet", index=False)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = {"executado_em": date.today().isoformat(), "metricas": metrics, "linhas_silver": len(employees)}
    (REPORT_DIR / "data_quality_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Camada Silver criada com {len(employees)} colaboradores.")


if __name__ == "__main__":
    run()
