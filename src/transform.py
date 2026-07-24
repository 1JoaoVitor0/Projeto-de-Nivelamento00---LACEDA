import pandas as pd

def transform_salary(df: pd.DataFrame) -> pd.DataFrame:
    if 'salario_base' not in df.columns:
        return df
    df['salario_base'] = (
                            df['salario_base']
                            .str.replace('R$', '', regex=False)
                            .str.replace(',', '.', regex=False)
                            .astype(float)
                        )
    return df

def transform_date(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if 'data' in col:
            df[col] = pd.to_datetime(df[col], format='mixed', dayfirst=True)
    return df

def verify_missing_values(df: pd.DataFrame):
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            print(f"Coluna '{col}' possui {missing_count} valores ausentes.")

    if 'id_reporta_a' in df.columns:
        missing_count = df[df['id_reporta_a'].isna()]['nivel'].value_counts()

        for cargo, quantidade in missing_count.items():
            if cargo.lower() != 'sócio':
                print(f"[ERRO] Cargo '{cargo}' possui {quantidade} registros sem 'id_reporta_a'.")
            else:
                print(f"Cargo '{cargo}' possui {quantidade} registros sem 'id_reporta_a'.")

    if 'score_satisfacao' in df.columns:
        missing_count = df[(df['score_satisfacao'].isna()) & (df['status_atual'] == 'Ativo')]['data_admissao'].dt.year.value_counts()

        for ano, quantidade in missing_count.items():
            print(f"Ano {ano}: {quantidade} registros sem 'score_satisfacao'.")
        


def transform_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    if 'id_reporta_a' in df.columns:
        df['id_reporta_a'] = df['id_reporta_a'].fillna(-1).astype(int)

    return df

