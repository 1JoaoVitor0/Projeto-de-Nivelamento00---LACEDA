import json

import pandas as pd

from config import GOLD_DIR, REFERENCE_DATE, REPORT_DIR, SILVER_DIR


def create_gold(employees: pd.DataFrame, departments: pd.DataFrame, branches: pd.DataFrame) -> pd.DataFrame:
    reference_date = pd.Timestamp(REFERENCE_DATE)
    gold = employees.merge(departments, on="id_departamento", how="left", validate="many_to_one")
    gold = gold.merge(branches, on="id_filial", how="left", validate="many_to_one")
    gold["desligado_flag"] = (gold["status_atual"] == "Desligado").astype("int8")
    gold["tempo_casa_dias"] = (reference_date - gold["data_admissao"]).dt.days
    gold["tempo_casa_anos"] = (gold["tempo_casa_dias"] / 365.25).round(2)
    gold["foi_promovido"] = gold["data_promocao"].notna()
    gold["dias_desde_promocao"] = (reference_date - gold["data_promocao"]).dt.days
    gold["salario_total_estimado"] = (gold["salario_base"] * (1 + gold["percentual_bonus"] / 100)).round(2)
    gold["faixa_horas_extras"] = pd.cut(gold["horas_extras_mes"], [-1, 10, 25, float("inf")], labels=["Baixa (0-10)", "Media (11-25)", "Alta (26+)"])
    gold["faixa_satisfacao"] = pd.cut(gold["score_satisfacao"], [0, 2.5, 3.5, 5], labels=["Baixa (1-2,5)", "Media (2,6-3,5)", "Alta (3,6-5)"])
    gold["faixa_tempo_casa"] = pd.cut(gold["tempo_casa_anos"], [-1, 1, 3, float("inf")], labels=["Ate 1 ano", "1 a 3 anos", "Mais de 3 anos"])
    return gold


def run() -> None:
    employees = pd.read_parquet(SILVER_DIR / "funcionarios.parquet")
    departments = pd.read_parquet(SILVER_DIR / "departamentos.parquet")
    branches = pd.read_parquet(SILVER_DIR / "filiais.parquet")
    gold = create_gold(employees, departments, branches)
    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    gold.to_parquet(GOLD_DIR / "evasao_colaboradores.parquet", index=False)
    report_path = REPORT_DIR / "data_quality_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report.update({"data_referencia_analise": REFERENCE_DATE, "linhas_gold": len(gold), "taxa_evasao": round(float(gold["desligado_flag"].mean()), 4)})
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Camada Gold criada com {len(gold)} colaboradores.")


if __name__ == "__main__":
    run()
