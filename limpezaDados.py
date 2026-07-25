'''Importando libs e dados'''

import pandas as pd

df_funcionarios = pd.read_csv("dados/funcionarios.csv")

'''Limpando os dados'''

df_funcionarios = df_funcionarios.drop_duplicates()

df_funcionarios['id_reporta_a'] = df_funcionarios['id_reporta_a'].astype('Int64')
df_funcionarios['data_admissao'] = pd.to_datetime(df_funcionarios['data_admissao'],errors="coerce",format='mixed',dayfirst=True)
df_funcionarios['data_promocao'] = pd.to_datetime(df_funcionarios['data_promocao'],errors="coerce",format='mixed',dayfirst=True)
df_funcionarios['nome'] = df_funcionarios['nome'].str.rsplit(' ', n=1).str[0]

df_funcionarios['salario_base'] = df_funcionarios['salario_base'].astype('str')

def padronizar_salarios(valor):
  valor = valor.replace('R$','')
  valor = valor.replace(' ','')
  valor = valor.replace(',','.')
  return valor

df_funcionarios['salario_base'] = df_funcionarios['salario_base'].apply(padronizar_salarios)
df_funcionarios['salario_base'] = df_funcionarios['salario_base'].astype('float')
df_funcionarios['score_satisfacao'] = df_funcionarios.groupby('id_departamento')['score_satisfacao'].transform(lambda x: x.fillna(x.mean())).round(1)

def padronizar_genero(valor):
  if valor == 'Fem':
    return 'Feminino'
  else:
    return valor

df_funcionarios['genero'] = df_funcionarios['genero'].apply(padronizar_genero)
df_funcionarios.to_csv("dados/funcionarios_limpo.csv", index=False)