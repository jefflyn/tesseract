import numpy as np
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt


X, y = datasets.make_classification(n_samples=1000, n_features=10, n_redundant=0)
dt = DecisionTreeClassifier()
dt.fit(X, y)

preds = dt.predict(X)
meanval = (y == preds).mean()
print(meanval)

n_features = 200
X, y = datasets.make_classification(750, n_features, n_informative=5)
print((X, y))

training = np.random.choice([True, False], p=[.75, .25], size=len(y))
print(training)
accuracies = []
for x in np.arange(1, n_features+1):
    dt = DecisionTreeClassifier(max_depth=x)
    dt.fit(X[training], y[training])
    preds = dt.predict(X[~training])
    accuracies.append((preds == y[~training]).mean())

f, ax = plt.subplots(figsize=(7, 5))
ax.plot(range(1, n_features + 1), accuracies, color='k')
ax.set_title("Decision Tree Accuracy")
ax.set_ylabel("% Correct")
ax.set_xlabel("Max Depth")
