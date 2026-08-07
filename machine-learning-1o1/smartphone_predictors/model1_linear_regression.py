import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

print("=== MODEL 1: LINEAR REGRESSION ===")
# 1. Load Data
df = pd.read_csv("used_smartphone_prices.csv")

# 2. Split Data
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

# 3. Separate Clues and Answer
y_train = df_train['Resale_Price_INR']
y_test = df_test['Resale_Price_INR']

columns_to_drop = ['Resale_Price_INR', 'Cover_Color_ID', 'IMEI_Last_Digit', 'Pincode_Last_Digit']
X_train = df_train.drop(columns=columns_to_drop)
X_test = df_test.drop(columns=columns_to_drop)

# 4. Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Check Error
mae = mean_absolute_error(y_test, model.predict(X_test))
print(f"Error: Off by {mae:.0f} Rupees on average\n")

# 6. Clue Scoreboard (Linear Regression uses 'coefficients' or weights)
print("--- CLUE SCOREBOARD (Weights) ---")
importance = pd.DataFrame({'Clue': X_train.columns, 'Weight': model.coef_})
print(importance.sort_values(by='Weight', key=abs, ascending=False).to_string(index=False))

# 7. Single Row Prediction
print("\n--- Single Prediction ---")
new_phone = pd.DataFrame({'RAM_GB': [6], 'Storage_GB': [128], 'Age_In_Months': [12.0], 'Battery_Capacity_mAh': [4500], 'Camera_MP': [48]})
print(f"Predicted Price: {model.predict(new_phone)[0]:.0f} Rupees")
