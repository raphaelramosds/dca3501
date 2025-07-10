from abc import ABC
from typing import Type
from urllib.parse import urlparse
import pandas as pd
import os


class DataLoader(ABC):
    def load(self, path: str) -> pd.DataFrame:
        raise NotImplementedError


class NormalCSVLoader(DataLoader):
    def load(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path, header=None, skipinitialspace=True)


class SkipLineCSVLoader(DataLoader):
    def load(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path, skiprows=1, header=None, skipinitialspace=True)


class IncomeDataset:

    columns = [
        "age",
        "workclass",
        "fnlwgt",
        "education",
        "education_num",
        "marital_status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "capital_gain",
        "capital_loss",
        "hours_per_week",
        "native_country",
        "high_income",
    ]
    categoric = [
        "workclass",
        "education",
        "marital_status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native_country",
        "high_income",
    ]
    features = [
        "age",
        "workclass",
        "education_num",
        "marital_status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "hours_per_week",
        "native_country",
    ]
    label = "high_income"

    def __init__(self, url: str, data_loader_cls: Type[DataLoader]):
        self.__url = url
        self.__data_loader_cls = data_loader_cls
        self.__load()
        self.__transform()

        # Separar matriz de features do vetor de labels
        self.data = self.__income[IncomeDataset.features]
        self.target = self.__income[IncomeDataset.label]

    def __load(self) -> pd.DataFrame:
        """
        Carrega dataset da URL para arquivo local (se ainda não existir),
        e depois lê a versão local.
        """
        current_dir = os.path.dirname(__file__)
        filename = os.path.basename(urlparse(self.__url).path)
        local_file = os.path.join(current_dir, filename)

        if not os.path.exists(local_file):
            self.__data_loader_cls.load(self.__url).to_csv(
                local_file, header=False, index=False
            )

        self.__income = self.__data_loader_cls.load(local_file)

    def __transform(self) -> pd.DataFrame:
        """
        Prepara o DataFrame:
        - Define nomes das colunas
        - Converte colunas categóricas em códigos numéricos
        """
        self.__income.reset_index(drop=True, inplace=True)
        self.__income.columns = IncomeDataset.columns
        for column_name in IncomeDataset.categoric:
            self.__income[column_name] = (
                self.__income[column_name].astype("category").cat.codes
            )


def load_income_test():
    return IncomeDataset(
        "http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test",
        SkipLineCSVLoader(),
    )


def load_income_train():
    return IncomeDataset(
        "http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
        NormalCSVLoader(),
    )
