from pathlib import Path

import pandas as pd


def read_csv(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, encoding="utf-8")
    frame.columns = frame.columns.str.strip()
    for column in frame.select_dtypes(include="object"):
        frame[column] = frame[column].str.strip().replace({"": pd.NA, "NULL": pd.NA, "null": pd.NA})
    return frame


def parse_date(series: pd.Series) -> pd.Series:
    text = series.astype("string").str.strip()
    iso = pd.to_datetime(text.where(text.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)), format="%Y-%m-%d", errors="coerce")
    br = pd.to_datetime(text.where(text.str.match(r"^\d{2}/\d{2}/\d{4}$", na=False)), format="%d/%m/%Y", errors="coerce")
    return iso.fillna(br)


def parse_currency(series: pd.Series) -> pd.Series:
    text = series.astype("string").str.replace(r"[^0-9,.-]", "", regex=True)
    has_comma_and_dot = text.str.contains(",", na=False) & text.str.contains(r"\.", regex=True, na=False)
    has_only_comma = text.str.contains(",", na=False) & ~text.str.contains(r"\.", regex=True, na=False)
    text = text.where(~has_comma_and_dot, text.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    text = text.where(~has_only_comma, text.str.replace(",", ".", regex=False))
    return pd.to_numeric(text, errors="coerce")
