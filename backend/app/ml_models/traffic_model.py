# population_model.pkl
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

X = np.array([[1],[2],[3],[4],[5]])
y = np.array([1000,1200,1500,1800,2100])
model = LinearRegression().fit(X, y)
joblib.dump(model, "traffic_model.py")
