from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier

X, y = datasets.make_classification(n_samples=1000, n_features=3, n_redundant=0)
dt = DecisionTreeClassifier()
print(dt)
dt.fit(X, y)

preds = dt.predict(X)
meanval = (y == preds).mean()
print(meanval)