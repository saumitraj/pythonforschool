import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import TransformedTargetRegressor
from sklearn.metrics import mean_absolute_error

# ---------------------------------------------------------
# 1. SETUP & FEATURE SELECTION
# ---------------------------------------------------------
print("--- 1. Loading and Prepping Data ---")
df = pd.read_csv("used_smartphone_prices_old.csv")

# Split the data first to keep the test group fair and locked
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

# Define Target
y_train = df_train['Resale_Price_INR']
y_test = df_test['Resale_Price_INR']

# Define Features
columns_to_drop = ['Resale_Price_INR', 'Cover_Color_ID', 'IMEI_Last_Digit', 'Pincode_Last_Digit']
X_train = df_train.drop(columns=columns_to_drop)
X_test = df_test.drop(columns=columns_to_drop)

print(f"Training on {len(X_train)} phones, Testing on {len(X_test)} phones.\n")

# ---------------------------------------------------------
# 2. THE GREAT MODEL SHOWDOWN
# ---------------------------------------------------------
print("--- 2. The Great Model Showdown ---")

# Model 1: Linear Regression
model_1 = LinearRegression()
model_1.fit(X_train, y_train)
err_1 = mean_absolute_error(y_test, model_1.predict(X_test))

# Model 2: Decision Tree
model_2 = DecisionTreeRegressor(random_state=42)
model_2.fit(X_train, y_train)
err_2 = mean_absolute_error(y_test, model_2.predict(X_test))

# Model 3: Random Forest
model_3 = RandomForestRegressor(random_state=42)
model_3.fit(X_train, y_train)
err_3 = mean_absolute_error(y_test, model_3.predict(X_test))

# Model 4: Neural Network (MLP) with both Feature & Target Scaling
base_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('mlp', MLPRegressor(
        hidden_layer_sizes=(64, 32),
        activation='relu',
        solver='adam',
        alpha=0.01,
        learning_rate_init=0.005,
        max_iter=1000,
        random_state=42
    ))
])

# TransformedTargetRegressor automatically scales y for training,
# and inverts the scaling back to INR when running .predict()
model_4 = TransformedTargetRegressor(
    regressor=base_pipeline,
    transformer=StandardScaler()
)

model_4.fit(X_train, y_train)
err_4 = mean_absolute_error(y_test, model_4.predict(X_test))

# ---------------------------------------------------------
# 3. THE RESULTS
# ---------------------------------------------------------
print(f"1. Linear Regression Error : Off by ₹{err_1:.0f} on average")
print(f"2. Decision Tree Error     : Off by ₹{err_2:.0f} on average")
print(f"3. Random Forest Error     : Off by ₹{err_3:.0f} on average")
print(f"4. Neural Network Error    : Off by ₹{err_4:.0f} on average\n")

# ---------------------------------------------------------
# 4. SINGLE ROW PREDICTION
# ---------------------------------------------------------
print("--- 3. Let's Predict a New Phone! ---")
new_phone = pd.DataFrame({
    'RAM_GB': [8],
    'Storage_GB': [256],
    'Age_In_Months': [24.0],
    'Battery_Capacity_mAh': [5000],
    'Camera_MP': [64]
})

# Align columns to match training set
new_phone = new_phone[X_train.columns]

predicted_rf = model_3.predict(new_phone)
predicted_nn = model_4.predict(new_phone)

print(f"Random Forest predicts this phone will sell for : ₹{predicted_rf[0]:.0f}")
print(f"Neural Network predicts this phone will sell for: ₹{predicted_nn[0]:.0f}")