import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# ---------------------------------------------------------
# 1. SETUP & FEATURE SELECTION
# ---------------------------------------------------------
print("--- 1. Loading and Prepping Data ---")
df = pd.read_csv("used_smartphone_prices.csv")

# Split the data first to keep the test group fair and locked
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

# Define Target (What we want to predict)
y_train = df_train['Resale_Price_INR']
y_test = df_test['Resale_Price_INR']

# Define Features (Dropping the answer and the useless noise)
columns_to_drop = ['Resale_Price_INR', 'Cover_Color_ID', 'IMEI_Last_Digit', 'Pincode_Last_Digit']
X_train = df_train.drop(columns=columns_to_drop)
X_test = df_test.drop(columns=columns_to_drop)

print(f"Training on {len(X_train)} phones, Testing on {len(X_test)} phones.\n")


# ---------------------------------------------------------
# 2. THE GREAT MODEL SHOWDOWN
# ---------------------------------------------------------
print("--- 2. The Great Model Showdown ---")

# Model 1: Linear Regression (The Strict Straight Line)
model_1 = LinearRegression()
model_1.fit(X_train, y_train)
preds_1 = model_1.predict(X_test)
err_1 = mean_absolute_error(y_test, preds_1)

# Model 2: Decision Tree (The Flowchart)
model_2 = DecisionTreeRegressor(random_state=42)
model_2.fit(X_train, y_train)
preds_2 = model_2.predict(X_test)
err_2 = mean_absolute_error(y_test, preds_2)

# Model 3: Random Forest (The Voting Council of 100 Trees)
model_3 = RandomForestRegressor(random_state=42)
model_3.fit(X_train, y_train)
preds_3 = model_3.predict(X_test)
err_3 = mean_absolute_error(y_test, preds_3)


# ---------------------------------------------------------
# 3. THE RESULTS
# ---------------------------------------------------------
print(f"1. Linear Regression Error : Off by ₹{err_1:.0f} on average")
print(f"2. Decision Tree Error     : Off by ₹{err_2:.0f} on average")
print(f"3. Random Forest Error     : Off by ₹{err_3:.0f} on average\n")


# ---------------------------------------------------------
# 4. SINGLE ROW PREDICTION (Using the winning model)
# ---------------------------------------------------------
print("--- 3. Let's Predict a New Phone! ---")
# Example: 8GB RAM, 256GB Storage, 24 months old, 5000mAh battery, 64MP camera
new_phone = pd.DataFrame({
    'RAM_GB': [8],
    'Storage_GB': [256],
    'Age_In_Months': [24.0],
    'Battery_Capacity_mAh': [5000],
    'Camera_MP': [64]
})

# We use model_3 because Random Forest usually wins!
predicted_price = model_3.predict(new_phone)
print(f"Random Forest predicts this phone will sell for: ₹{predicted_price[0]:.0f}")