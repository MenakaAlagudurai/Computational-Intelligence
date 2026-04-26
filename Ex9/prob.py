def get_float(prompt):
    while True:
        try:
            val = float(input(prompt))
            if 0 <= val <= 1:
                return val
            else:
                print("Enter probability between 0 and 1!")
        except:
            print("Invalid input!")


# Step 1: Compute Joint Probabilities
def compute_joint():
    print("\nEnter Joint Probabilities for Marketing Problem:")

    print("\nUse probabilities like:")
    print("Purchased + Ad Seen")
    print("Purchased + Ad Not Seen")
    print("Not Purchased + Ad Seen")
    print("Not Purchased + Ad Not Seen\n")

    joint = {}

    # Taking input from user
    joint[(1, 1)] = get_float("P(Purchased, Ad Seen): ")
    joint[(1, 0)] = get_float("P(Purchased, Ad Not Seen): ")
    joint[(0, 1)] = get_float("P(Not Purchased, Ad Seen): ")
    joint[(0, 0)] = get_float("P(Not Purchased, Ad Not Seen): ")

    total = sum(joint.values())

    if abs(total - 1.0) > 0.001:
        print("\nWarning: Total probability is not 1.")
        print("Current Total =", total)

    print("\n--- Joint Probability Table ---")
    print("P(Purchased, Ad Seen)       =", joint[(1, 1)])
    print("P(Purchased, Ad Not Seen)   =", joint[(1, 0)])
    print("P(Not Purchased, Ad Seen)   =", joint[(0, 1)])
    print("P(Not Purchased, Ad Not Seen) =", joint[(0, 0)])

    return joint


# Step 2: Simple Probability
def simple_prob(joint):
    print("\n--- Simple Probability ---")

    pA = joint[(1, 1)] + joint[(1, 0)]   # Purchased
    pB = joint[(1, 1)] + joint[(0, 1)]   # Ad Seen

    print("P(Purchased) =", pA)
    print("P(Ad Seen) =", pB)

    return pA, pB


# Step 3: Joint Inference
def joint_inference(joint, pA, pB):
    print("\n--- Joint Probability Inference ---")

    p_and = joint[(1, 1)]   # Purchased AND Ad Seen
    p_or = pA + pB - p_and
    p_notA = 1 - pA
    pA_given_B = p_and / pB if pB != 0 else 0

    print("P(Purchased AND Ad Seen) =", p_and)
    print("P(Purchased OR Ad Seen) =", p_or)
    print("P(Not Purchased) =", p_notA)
    print("P(Purchased | Ad Seen) =", pA_given_B)

    return pA_given_B


# Step 4: Bayes Probability
def bayes(pA, pB, pA_given_B):
    print("\n--- Bayes Probability ---")

    if pA == 0:
        print("Cannot compute Bayes (division by zero)")
        return

    pB_given_A = (pA_given_B * pB) / pA

    print("P(Ad Seen | Purchased) =", pB_given_A)


# MAIN
def main():
    joint = compute_joint()

    while True:
        print("\n====== MENU ======")
        print("1. Simple Probability")
        print("2. Joint Inference")
        print("3. Bayes Probability")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            pA, pB = simple_prob(joint)

        elif choice == '2':
            pA, pB = simple_prob(joint)
            pA_given_B = joint_inference(joint, pA, pB)

        elif choice == '3':
            pA, pB = simple_prob(joint)
            pA_given_B = joint_inference(joint, pA, pB)
            bayes(pA, pB, pA_given_B)

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()