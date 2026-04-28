import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# Step 1: Load Dataset
file_path = input("Enter CSV file path: ")
data = pd.read_csv(file_path)

# NEW: Fix for categorical data
# This converts all string labels into numbers so the model can read them
le = LabelEncoder()
for col in data.columns:
    data[col] = le.fit_transform(data[col])

# Step 2: Dataset Info
print("\n--- Dataset Information ---")
print("Total Records:", data.shape[0])
print("Total Features:", data.shape[1] - 1)  # excluding target

# Step 3: Split Features & Target
X = data.iloc[:, :-1].values   # all columns except last
y = data.iloc[:, -1].values    # last column as target

# Step 4: User Inputs
n_trees = int(input("\nEnter number of trees: "))
criterion = input("Enter criterion (gini/entropy): ").lower()
train_percent = float(input("Enter training percentage (e.g., 80): "))

test_size = 1 - (train_percent / 100)

# Step 5: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42
)

# Step 6: Model
model = RandomForestClassifier(
    n_estimators=n_trees,
    criterion=criterion,
    random_state=42
)

# Step 7: Train
model.fit(X_train, y_train)

# Step 8: Predict
y_pred = model.predict(X_test)

# Step 9: Evaluation Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
cm = confusion_matrix(y_test, y_pred)

print("\n--- Evaluation Metrics ---")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

print("\nConfusion Matrix:")
print(cm)

# Step 10: K-Fold Cross Validation
k_input = input("\nEnter number of folds for K-Fold: ")
k = int(k_input)

kfold = KFold(n_splits=k, shuffle=True, random_state=42)

cv_scores = cross_val_score(model, X, y, cv=kfold, scoring='accuracy')

print("\n--- K-Fold Results ---")
print("Accuracies for each fold:", cv_scores)
print("Mean Accuracy:", np.mean(cv_scores))