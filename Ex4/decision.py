import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from collections import Counter
from math import log2

# ---------------- ENTROPY FUNCTIONS ----------------
def entropy(y):
    total = len(y)
    counts = Counter(y)
    ent = 0
    for count in counts.values():
        p = count / total
        ent -= p * log2(p)
    return ent

def weighted_entropy(X, y, feature_idx):
    total = len(y)
    values = set(X[:, feature_idx])
    w_entropy = 0
    for val in values:
        subset_y = y[X[:, feature_idx] == val]
        w_entropy += (len(subset_y)/total) * entropy(subset_y)
    return w_entropy

# ---------------- INPUT FUNCTION ----------------
def getting_input():
    print("\nInput Method")
    print("1. Manual Input")
    print("2. CSV File Input")
    ch = int(input("Enter choice: "))

    # -------- MANUAL INPUT --------
    if ch == 1:
        n_attr = int(input("Enter number of attributes: "))
        n_obs = int(input("Enter number of observations: "))

        X, y = [], []

        print("\nEnter attribute values separated by space")
        for i in range(n_obs):
            X.append(list(map(float, input(f"Attributes for sample {i+1}: ").split())))
            y.append(int(input("Class label: ")))

        return np.array(X), np.array(y), None, None, 1

    # -------- CSV INPUT --------
    elif ch == 2:
        file = input("Enter CSV filename: ")
        df = pd.read_csv(file)

        print("\nColumns in dataset:")
        for i, col in enumerate(df.columns):
            print(f"{i} : {col}")

        feature_idx = list(map(int, input("\nEnter feature column indices (space separated): ").split()))
        target_idx = int(input("Enter target column index: "))

        X = df.iloc[:, feature_idx].values
        y = df.iloc[:, target_idx].values

        train_percent = int(input("Enter training percentage: "))
        feature_names = df.columns[feature_idx]

        return X, y, train_percent, feature_names, 2

    else:
        print("Invalid choice!")
        exit()

# ---------------- MAIN PROGRAM ----------------
data = getting_input()

# -------- MANUAL MODE --------
if data[4] == 1:
    X, y = data[0], data[1]

    # Train Decision Tree
    model = DecisionTreeClassifier(criterion="entropy", random_state=42)
    model.fit(X, y)
    preds = model.predict(X)

    # Root node
    root_feature_index = model.tree_.feature[0]

    # Entropy and Information Gain calculation
    init_entropy = entropy(y)
    w_entropy = weighted_entropy(X, y, root_feature_index)
    IG = init_entropy - w_entropy

    print("\nRoot Node Feature Index:", root_feature_index)
    print(f"Initial Entropy      : {init_entropy:.4f}")
    print(f"Weighted Entropy     : {w_entropy:.4f}")
    print(f"Information Gain (IG): {IG:.4f}")

    # Performance metrics
    print("Accuracy :", accuracy_score(y, preds))
    print("Precision:", precision_score(y, preds, average="macro"))
    print("Recall   :", recall_score(y, preds, average="macro"))
    print("F1 Score :", f1_score(y, preds, average="macro"))

# -------- CSV MODE --------
else:
    X, y, train_percent, feature_names = data[0], data[1], data[2], data[3]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=1 - train_percent / 100, random_state=42
    )

    model = DecisionTreeClassifier(criterion="entropy", random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    root_feature_index = model.tree_.feature[0]
    root_feature_name = feature_names[root_feature_index]

    print("\nRoot Node:", root_feature_name)
    print("Accuracy :", accuracy_score(y_test, preds))
    print("Precision:", precision_score(y_test, preds, average="macro"))
    print("Recall   :", recall_score(y_test, preds, average="macro"))
    print("F1 Score :", f1_score(y_test, preds, average="macro"))