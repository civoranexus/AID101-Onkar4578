import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# IMPORTANT: specify tab separator
data = pd.read_csv('../datasets/crop_yield_large.csv', sep='\t')

# Normalize column names
data.columns = data.columns.str.strip().str.lower()

print("Columns:", data.columns)

# Select features
X = data[['rainfall', 'temperature', 'soil_quality']]
y = data['yield']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open('yield_model.pkl', 'wb'))

print("Yield prediction model trained successfully using large dataset")
