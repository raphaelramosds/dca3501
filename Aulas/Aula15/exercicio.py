import pandas as pd

income_test = pd.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test", header=1)

# Inclusão dos títulos das colunas
income_test.columns = ["age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain","capital_loss", "hours_per_week", "native_country", "high_income"]

# Conversão das variáveis categóricas textuais para numéricas
for col_name in income_test.columns:
    income_test[col_name] = income_test[col_name].astype('category').cat.codes