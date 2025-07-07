import pandas as pd

# Carregue os arquivos no seguinte github: dados do EU.
# https://github.com/jakevdp/data-USstates/

pop = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-population.csv')
areas = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-areas.csv')
abbrevs = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-abbrevs.csv')

"""
Passo 1. Gere um DataFrame (df_merged), com as seguintes colunas:

Colunas: `state/region`, `ages`, `year`, `population`, `state`

Depois, faça as seguintes verificações

- Verificação das cinco primeiras linhas do DataFrame gerado
- Verificação se há algum dado faltando
- Verificação de quais itens de "population" estão faltando
- Verificação de quais `state/region` têm elementos na coluna `state` com data missing
"""

# O conteudo da coluna state/region (left table) se associa com a coluna abbreviation (right table)
df_merged = pd.merge(pop, abbrevs, how="outer", left_on='state/region', right_on='abbreviation')

print("Verificação das cinco primeiras linhas do DataFrame gerado")
print(df_merged.head(), "\n")

print("Verificação se há algum dado faltando")
print(df_merged.isna().any(), "\n")

print("Check the rows of population with missing values")
print(df_merged[df_merged['population'].isna()].head(), "\n")

print("Verificação de quais itens de \"population\" estão faltando")
print(
    # Explicação:
    # 1. Recupera as linhas em que `state` é null
    # 2. Extrai apenas a coluna `state/region` dessas linhas
    # 3. Lista apenas valores diferentes (únicos) de `state/region`
    df_merged.loc[df_merged['state'].isnull(), 'state/region'].unique()
, "\n")

print("EXTRA. Preencha a coluna `state`: United States caso `state/region` seja US, e Puerto Rico caso seja PR")
df_merged.loc[df_merged['state/region'] == 'US', 'state'] = 'United States'
df_merged.loc[df_merged['state/region'] == 'PR', 'state'] = 'Puerto Rico'
print(df_merged[df_merged['state/region'].isin(['US', 'PR'])].head(), "\n")

"""
Passo 2. Gere um DataFrame (df_final), com as seguintes colunas:

Colunas `state/region`, `ages`, `year`, `population`, `state`, `area (sq. mi)`

Depois faça as seguintes verificações
- Verificação do resultado
- Verificação se há data missing
"""

df_final = pd.merge(df_merged, areas, on='state', how='left')

print("Verificação do resultado")
print(df_final.head(), "\n")

print("Verificação se há data missing")
print(df_final.isna().any(), "\n")

"""
Passo 3. Deve haver nulos na coluna da área.

Verifique quais regiões foram ignoradas.
"""

print("`state/region` com valores faltantes na coluna `area` (sq. mi)")
print(df_final['state/region'][df_final['area (sq. mi)'].isnull()].unique())

"""
Passo 4. Há campos na coluna de área no DataFrame com data missing.

Para resolver esse tipo de problema, podemos inserir o valor apropriado (usando a soma de todas as 
áreas de estado, por exemplo), mas neste caso, simplesmente elimite os campos com valores nulos.
"""

# Preencher areas faltantes com 0.0
df_final.loc[df_final['area (sq. mi)'].isnull(), 'area (sq. mi)'] = 0

print("Como é possível observar, area (sq. mi) não possui mais dados faltantes")
print(df_final[df_final['state/region'].isin(['USA'])].head(), "\n")
print(df_final.isna().any(), "\n")

"""
Passo 5. Obtenha um DataFrame (data2010) da população dos EU em 2010 (apenas o total por estados).

data2010(state/region, ages, year, population, state,area (sq. mi))
"""

data2010 = df_final.query("year == 2010 & ages == 'total'")
data2010.head()

"""
Passo 6. Obtenha os 5 estados com maiores densidades populacionais em 2010 (em order decrescente)
"""

def sort_df(df : pd.DataFrame, col : str, asc : bool = True) -> pd.DataFrame:
    """
    Ordena uma cópia de um DataFrame por uma coluna específica e a retorna.
    """
    df_copy = df.copy()
    return df_copy.sort_values(by=col, ascending=asc)

print("Top-5 estados com maiores densidades populacionais em 2010 (em order decrescente)")
print(sort_df(data2010, 'population', False)[:5][['state', 'population']], "\n")

"""
Passo 7. Obtenha os 5 estados com menores densidades populacionais em 2010 (em order decrescente)
"""

print("Top-5 estados com menores densidades populacionais em 2010 (em order decrescente)")
print(sort_df(data2010, 'population')[:5][['state', 'population']], "\n")

"""
Passo 8. Obtenha os 05 estados com maiores proporções de jovens (under 18) em 2010 (apresente o resultado em ordem decrescente)
"""

# Montar DataFrame contendo dados de idades abaixo de 18
data2010_under18 = df_final.query("year == 2010 & ages == 'under18'")

print("Top-5 estados com maiores proporções de jovens (under 18) em 2010 (apresente o resultado em ordem decrescente)")
print(sort_df(data2010_under18, 'population', False)[:5][['state', 'population']], "\n")

"""
Passo 9. Obtenha a média das populações (total e under18) por estado.

- Sugestão: Utilizar groupBy.
"""

def groupby_mean(df: pd.DataFrame, group_col: str, data_col: str) -> pd.Series:
    """
    Agrupa um DataFrame por uma coluna específica e calcula a média da coluna de dados especificada.
    """
    df_copy = df.copy()
    return df_copy.groupby(by=group_col)[data_col].mean()

# Concatenar medias de `total` e `under18`
state_pop_mean = pd.concat(
    [
        groupby_mean(data2010, 'state', 'population'),
        groupby_mean(data2010_under18, 'state', 'population'),
    ],
    axis=1
)

# Renomear colunas
state_pop_mean.columns = ['mean total', 'mean under18']

print("Média das populações (total e under18) por estado.", "\n")
print(state_pop_mean)