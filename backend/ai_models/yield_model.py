import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle


data = pd.read_csv('../datasets/crop_yield_large.csv', sep='\t')


data.columns = data.columns.str.strip().str.lower()

print("Columns:", data.columns)


X = data[['rainfall', 'temperature', 'soil_quality']]
y = data['yield']


model = LinearRegression()
model.fit(X, y)


pickle.dump(model, open('yield_model.pkl', 'wb'))

print("Yield prediction model trained successfully using large dataset")
