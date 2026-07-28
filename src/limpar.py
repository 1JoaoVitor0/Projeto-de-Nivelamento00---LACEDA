import pandas as pd
import unicodedata
import numpy as np


entrada = "funcionarios.csv"
saida = "funcionarios_.csv"

#leroexcel

df = pd.read_csv(
    entrada,
    sep=",",
    encoding="utf-8",
    dtype=str,
    keep_default_na=False
)

#correçao enconding 

def corrigir_texto(valor):
    if not isinstance(valor, str):
        return valor

    try:
        return valor.encode("latin1").decode("utf-8")
    except:
        return valor


for coluna in df.columns:
    df[coluna] = df[coluna].apply(corrigir_texto)


#limpar

df = df.applymap(
    lambda x: x.strip() if isinstance(x, str) else x
)

#correcaogenero

df["genero"] = df["genero"].replace({
    "Fem": "Feminino",
    "Mas": "Masculino"
})


#data

for col in ["data_admissao", "data_promocao"]:

    df[col] = pd.to_datetime(
        df[col],
        errors="coerce",
        dayfirst=True
    )

    df[col] = df[col].dt.strftime("%Y-%m-%d")

#salario

def limpar_salario(valor):

    if valor == "":
        return None

    valor = (
        valor
        .replace("R$", "")
        .replace(" ", "")
    )

   
    if "," in valor:
        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")

    return valor


df["salario_base"] = df["salario_base"].apply(limpar_salario)


#decimais

colunas_decimal = [
    "percentual_bonus",
    "score_satisfacao"
]


for col in colunas_decimal:
    df[col] = (
        df[col]
        .replace("", None)
    )


#boolean

df["home_office"] = df["home_office"].replace({
    "True": "1",
    "False": "0"
})


df = df.replace({
    "": np.nan
})


#exportacao

df.to_csv(
    saida,
    index=False,
    sep=",",
    encoding="utf-8",
    na_rep="\\N"
)


print("Arquivo gerado:", saida)
print(df.head())