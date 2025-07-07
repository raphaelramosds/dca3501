import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

digits = datasets.load_digits()

# Trate a base de dados, como variáveis features e target.
X = digits['data']
y = digits['target']

# Separe os conjuntos de treinamento e teste (use o parâmetro test_size = 0.2)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.2)

# Treine como algorítmos K-NN, para k= 1,3,5,7.
k_values = np.arange(1, 9, 2)
knn_classifiers = [KNeighborsClassifier(n_neighbors=k) for k in k_values]
knn_results = tuple(zip(
    k_values, 
    [
        {
            'train' : knn.fit(X_train, y_train),
            'test' : knn.predict(X_test)
        } for knn in knn_classifiers
    ]
))

# Obtenha os escores dos resultados para esses valores de k
for kr in knn_results:
    k, results = kr
    score = np.mean(results['test'] == y_test)
    print("(k = {}) Test set score: {:.2f}".format(k, score))