import pandas as pd
import numpy as np
from math import sqrt
from collections import Counter, defaultdict
from tabulate import tabulate
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


# ---------------- Distance Functions ----------------
def euclidean(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def manhattan(a, b):
    return np.sum(np.abs(a - b))

def chebyshev(a, b):
    return np.max(np.abs(a - b))


# ---------------- Compute k ----------------
def compute_k(n):
    k = int(0.1 * n)
    if k % 2 == 0:
        k = k + 1
    if k == 0:
        k = 1
    return k


# ---------------- Input ----------------
def getting_input():
    print("\nInput Method")
    print("1. Manual Input")
    print("2. CSV File Input")
    ch = int(input("Enter choice: "))

    # -------- MANUAL --------
    if ch == 1:
        n_attr = int(input("Enter number of attributes: "))
        n_obs = int(input("Enter number of observations: "))

        X, y = [], []
        for _ in range(n_obs):
            X.append(list(map(float, input("Enter attributes: ").split())))
            y.append(int(input("Enter class label: ")))

        test_point = np.array(list(map(float, input("Enter test data point: ").split())))

        k = int(input("Enter value of k: "))

        print("\nDistance Method")
        print("1. Euclidean")
        print("2. Manhattan")
        print("3. Chebyshev")
        dch = int(input("Enter choice: "))

        print("1. Unweighted")
        print("2. Weighted")
        wch = int(input("Enter choice: "))

        return np.array(X), np.array(y), test_point, k, dch, wch, 1

    # -------- CSV --------
    elif ch == 2:
        file = input("Enter CSV filename: ")
        df = pd.read_csv(file)

        print("\nColumns in dataset:")
        for i, col in enumerate(df.columns):
            print(f"{i} : {col}")

        feature_idx = list(map(int, input(
            "\nEnter feature column indices (space separated): "
        ).split()))
        target_idx = int(input("Enter target column index: "))

        # -------- Numeric Validation --------
        try:
            X = df.iloc[:, feature_idx].astype(float).values
            y = df.iloc[:, target_idx].astype(int).values
        except ValueError:
            print("Error: Selected columns contain non-numeric data.")
            exit()

        train_percent = int(input("Enter training percentage: "))

        print("1. Unweighted")
        print("2. Weighted")
        wch = int(input("Enter choice: "))

        return X, y, None, None, 1, wch, train_percent

    else:
        print("Invalid choice")
        exit()


# ---------------- Custom KNN ----------------
def knn_classifier(X, y, test_point, k, dist_fn, weighted, show_steps):
    distances = []

    for i in range(len(X)):
        d = dist_fn(X[i], test_point)
        distances.append([i + 1, y[i], round(d, 3)])

    distances.sort(key=lambda x: x[2])
    neighbours = distances[:k]

    if show_steps:
        print("\nDistance Calculation")
        print(tabulate(distances,
                       headers=["No", "Class Label", "Distance"],
                       tablefmt="grid"))

        print(f"\nTop {k} Nearest Neighbours")
        print(tabulate(neighbours,
                       headers=["No", "Class Label", "Distance"],
                       tablefmt="grid"))

    # -------- UNWEIGHTED --------
    if not weighted:
        votes = Counter(row[1] for row in neighbours)

        if show_steps:
            table = [[cls, votes[cls]] for cls in votes]
            print("\nUnweighted Voting")
            print(tabulate(table,
                           headers=["Class Label", "Votes"],
                           tablefmt="grid"))

        return votes.most_common(1)[0][0]

    # -------- WEIGHTED (1/d²) --------
    weight_sum = defaultdict(float)
    weight_table = []

    for _, label, dist in neighbours:
        if dist == 0:
            weight = float('inf')
        else:
            weight = 1 / (dist ** 2)

        weight_sum[label] += weight
        weight_table.append([label, round(weight, 3)])

    if show_steps:
        print("\nWeights (1 / distance^2)")
        print(tabulate(weight_table,
                       headers=["Class Label", "Weight"],
                       tablefmt="grid"))

        final = [[cls, round(weight_sum[cls], 3)] for cls in weight_sum]
        print("\nWeighted Voting")
        print(tabulate(final,
                       headers=["Class Label", "Total Weight"],
                       tablefmt="grid"))

    return max(weight_sum, key=weight_sum.get)


# ---------------- MAIN ----------------
X, y, test_point, k, dch, wch, mode = getting_input()

weighted = (wch == 2)

# -------- MANUAL INPUT --------
if mode == 1:
    dist_fn = euclidean if dch == 1 else manhattan if dch == 2 else chebyshev
    result = knn_classifier(X, y, test_point, k, dist_fn, weighted, show_steps=True)
    print("\nNew data has class label:", result)

# -------- CSV INPUT --------
else:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=1 - mode / 100, random_state=1
    )

    k = compute_k(len(X_train))   # automatic k

    preds = []
    for tp in X_test:
        preds.append(
            knn_classifier(X_train, y_train, tp, k, euclidean, weighted, show_steps=False)
        )
   


    print("\nComputed k =", k)
    print("Accuracy:", accuracy_score(y_test, preds))
    print("Precision:", precision_score(y_test, preds, average="macro"))
    print("Recall:", recall_score(y_test, preds, average="macro"))
    print("F1 Score:", f1_score(y_test, preds, average="macro"))

    cm = confusion_matrix(y_test, preds)
    print("\nConfusion Matrix\n", cm)
    final_votes = Counter(preds)
    winning_class = final_votes.most_common(1)[0][0]
    print("\nFinal Winning Class Label:", winning_class)
    