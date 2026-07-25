import limpezaDados
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


df_funcionarios = limpezaDados.df_funcionarios

'''Criando novas colunas'''

df_funcionarios['ja_promovido'] = df_funcionarios['data_promocao'].notna()

data_referencia = pd.Timestamp.today()
df_funcionarios['tempo_empresa'] = (data_referencia - df_funcionarios['data_admissao']).dt.days / 365.25

df_funcionarios['desligado'] = (df_funcionarios['status_atual'] == 'Desligado').astype(int)


'''Extracao de informacoes'''

taxa_desligamento = (df_funcionarios['desligado'].mean() * 100).round(2)

print(f"Taxa de desligamento: {taxa_desligamento}%")

sb.heatmap(df_funcionarios.corr(numeric_only=True), annot=True)
plt.show() # aqui percebe-se que (mesmo com uma relação fraca) a correlação entre satisfação
#e desligamento é negativa, ou seja, quanto maior a satisfação, menor a chance de desligamento.

df_funcionarios.groupby('ja_promovido')['desligado'].mean().plot(kind='bar', title='Taxa de Desligamento por Status de Promoção', color='lightblue')
plt.show() #pessoas que foram promovidas tem uma taxa de desligamento menor do que as que não foram promovidas,
#o que indica que a promoção pode ser um fator de retenção de funcionários.

# satisfação por departamento
df_funcionarios.groupby('id_departamento')['score_satisfacao'].mean().plot(kind='bar', title='Média de Satisfação por Departamento', color='orange')
plt.show() #como padrão, funcionarios do departamento 20, tem uma menor satisfação, como a satisfação tem uma relação negativa com o desligamento,
#isso pode indicar que o departamento 20 tem uma maior taxa de desligamento.

# desligamento por departamento
df_funcionarios.groupby('id_departamento')['desligado'].mean().plot(kind='bar', title='Taxa de Desligamento por Departamento', color='lightcoral')
plt.show() #prova que o departamento 20 tem uma maior taxa de desligamento, o que pode indicar problemas de gestão ou cultura nesse departamento.

#promocao por departamento
df_funcionarios.groupby('id_departamento')['ja_promovido'].mean().plot(kind='bar', title='Taxa de Promoção por Departamento', color='lightgreen')
plt.show() #mostra que não é apenas um problema de falta de promoção, pois a taxa é semelhante aos outros

#horas extras por departamento
df_funcionarios.groupby('id_departamento')['horas_extras_mes'].mean().plot(kind='bar', title='Média de Horas Extras por Departamento', color='yellow')
plt.show() #mostra que o departamento 20 tem uma média de horas extras maior, que possui uma correlação
#positiva com o volume de processos jurídicos sob responsabilidade do advogado, o que indica que o departamento 20
#tem uma maior carga de trabalho, o que pode levar a uma maior insatisfação e, consequentemente, a uma maior taxa de desligamento.