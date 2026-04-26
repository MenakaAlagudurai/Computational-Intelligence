import numpy as np

# ---------------- Activation Functions ----------------
def threshold(x):
    return 1 if x >= 0 else 0

def bipolar_threshold(x):
    return 1 if x >= 0 else -1

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

# ---------------- User Inputs ----------------
alpha = float(input("Enter learning rate (alpha): "))
n = int(input("Enter number of inputs: "))

weights = np.array([float(input(f"Enter initial weight w{i+1}: ")) for i in range(n)])
b = float(input("Enter bias: "))

print("\nChoose Gate:")
print("1. AND\n2. OR\n3. NAND\n4. NOR\n5. XOR\n6. XNOR\n7. NOT")
gate_choice = int(input("Enter choice: "))

print("\nChoose Activation Function:")
print("1. Threshold\n2. Sigmoid\n3. Tanh")
act_choice = int(input("Enter choice: "))

# ---------------- USER ENTERS DATASET ----------------
print("\nEnter number of training samples:")
m = int(input())

inputs = []
print("Enter inputs row by row (space separated):")
for i in range(m):
    row = list(map(int, input().split()))
    inputs.append(row)

inputs = np.array(inputs)

# ---------------- AUTO DETECT INPUT TYPE ----------------
if np.any(inputs == -1):
    type_choice = 2
else:
    type_choice = 1

print("\nDetected Input Type:", "Bipolar (-1,1)" if type_choice == 2 else "Binary (0,1)")

# ---------------- TARGET GENERATION ----------------
targets = []

for x in inputs:
    temp = np.where(x == 1, 1, 0)  # convert to binary logic

    if gate_choice == 1:   # AND
        out = 1 if np.all(temp) else 0

    elif gate_choice == 2: # OR
        out = 1 if np.any(temp) else 0

    elif gate_choice == 3: # NAND
        out = 0 if np.all(temp) else 1

    elif gate_choice == 4: # NOR
        out = 0 if np.any(temp) else 1

    elif gate_choice == 5: # XOR
        out = np.sum(temp) % 2

    elif gate_choice == 6: # XNOR
        out = 0 if np.sum(temp) % 2 else 1

    elif gate_choice == 7: # NOT
        if n != 1:
            print("NOT gate requires 1 input")
            exit()
        out = 0 if temp[0] == 1 else 1

    # Convert to bipolar if needed
    if type_choice == 2:
        out = 1 if out == 1 else -1

    targets.append(out)

targets = np.array(targets)

# ---------------- Activation Selection ----------------
if act_choice == 1:
    act = threshold if type_choice == 1 else bipolar_threshold
elif act_choice == 2:
    act = sigmoid
elif act_choice == 3:
    act = tanh

# ---------------- Training ----------------
max_epochs = 20

print("\n================ TRAINING START ================\n")

for epoch in range(max_epochs):
    print(f"\n******** EPOCH {epoch+1} ********\n")

    no_update = True

    print("Inputs".ljust(15), "t   yin    y    weights    b")
    print("-"*70)

    for i in range(len(inputs)):
        x = inputs[i]
        t = targets[i]

        yin = np.dot(x, weights) + b
        y = act(yin)

        # Normalize output
        if act_choice == 2:
            y = 1 if y >= 0.5 else (0 if type_choice == 1 else -1)
        elif act_choice == 3:
            y = 1 if y >= 0 else (0 if type_choice == 1 else -1)

        # Weight update
        if y != t:
            weights = weights + alpha * t * x
            b = b + alpha * t
            no_update = False

        error = t - y

        print(f"{str(x):<15}{t:<4}{yin:<7.2f}{y:<5}{weights}{b:.2f}")

    if no_update:
        print("\nConverged!")
        break
else:
    print("\nDid NOT converge")

