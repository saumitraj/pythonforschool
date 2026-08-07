import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. Load the Dataset
print("--- 1. Loading Smartphone Data ---")
df = pd.read_csv("used_smartphone_prices.csv")
print(f"Total phones in dataset: {len(df)}\n")

# 2. Split the ENTIRE dataset to lock the rows
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

# 3. Separate the Target
y_train = df_train['Resale_Price_INR']
y_test = df_test['Resale_Price_INR']

# 4. Feature Selection (Dropping the noise and the target)
columns_to_drop = ['Resale_Price_INR', 'Cover_Color_ID', 'IMEI_Last_Digit', 'Pincode_Last_Digit']
X_train = df_train.drop(columns=columns_to_drop)
X_test = df_test.drop(columns=columns_to_drop)

# 5. Fit the Model
print("--- 2. Training Model ---")
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# 6. Overall Accuracy
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model Error: On average, the prediction is off by ₹{mae:.2f}\n")

# 7. Single Row Prediction (The Test Case)
print("--- 3. Single Phone Prediction ---")
# Let's invent a phone: 6GB RAM, 128GB Storage, 12 months old, 4500mAh battery, 48MP camera
new_phone = pd.DataFrame({
    'RAM_GB': [6],
    'Storage_GB': [128],
    'Age_In_Months': [12.0],
    'Battery_Capacity_mAh': [4500],
    'Camera_MP': [48]
})

predicted_price = model.predict(new_phone)
print(f"The model predicts this phone will sell for: ₹{predicted_price[0]:.0f}")



# Assuming you named your Random Forest model 'model' (or 'model_3')
# Let's see which clues the model thought were actually useful!

print("--- CLUE SCOREBOARD (Feature Importances) ---")

importance_scores = pd.DataFrame({
    'Clue (Feature)': X_train.columns,
    'Usefulness Score': model.feature_importances_
})

# Sort the scoreboard from highest to lowest
importance_scores = importance_scores.sort_values(by='Usefulness Score', ascending=False)

# Format it nicely so it's easy to read
importance_scores['Usefulness Score'] = importance_scores['Usefulness Score'].apply(lambda x: f"{x * 100:.1f}%")

print(importance_scores)