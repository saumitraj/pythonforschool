from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

print("--- HOW TO IMPROVE A MODEL ---")

# ---------------------------------------------------------
# Technique 1: Stopping the Tree from Overthinking
# ---------------------------------------------------------
print("\n1. Fixing the Decision Tree (Adding max_depth)")

# The old tree that overthinks
bad_tree = DecisionTreeRegressor(random_state=42)
bad_tree.fit(X_train, y_train)
bad_tree_err = mean_absolute_error(y_test, bad_tree.predict(X_test))

# The new tree limited to only 5 levels of questions
smart_tree = DecisionTreeRegressor(max_depth=5, random_state=42)
smart_tree.fit(X_train, y_train)
smart_tree_err = mean_absolute_error(y_test, smart_tree.predict(X_test))

print(f"Old Tree Error   : ₹{bad_tree_err:.0f}")
print(f"Smart Tree Error : ₹{smart_tree_err:.0f} (Better!)\n")


# ---------------------------------------------------------
# Technique 2: Growing a Bigger Forest
# ---------------------------------------------------------
print("2. Upgrading the Random Forest (Adding n_estimators)")

# A tiny forest with only 10 trees
small_forest = RandomForestRegressor(n_estimators=10, random_state=42)
small_forest.fit(X_train, y_train)
small_forest_err = mean_absolute_error(y_test, small_forest.predict(X_test))

# A massive forest with 200 trees
big_forest = RandomForestRegressor(n_estimators=200, random_state=42)
big_forest.fit(X_train, y_train)
big_forest_err = mean_absolute_error(y_test, big_forest.predict(X_test))

print(f"10-Tree Forest Error  : ₹{small_forest_err:.0f}")
print(f"200-Tree Forest Error : ₹{big_forest_err:.0f} (Even Better!)")