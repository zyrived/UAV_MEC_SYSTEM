import numpy as np


def apply_operator(sol, operator):
    if operator == 'Swap':
        # Select two distinct indices randomly
        idx1, idx2 = np.random.choice(len(sol), size=2, replace=False)
        # Swap the values at the selected indices
        sol[idx1], sol[idx2] = sol[idx2], sol[idx1]

    elif operator == 'Reversion':
        # Select a sub-route randomly (start and end indices)
        start_idx, end_idx = np.random.choice(len(sol), size=2, replace=False)
        if start_idx > end_idx:
            start_idx, end_idx = end_idx, start_idx
        # Reverse the order of the selected sub-route
        sol[start_idx:end_idx + 1] = sol[start_idx:end_idx + 1][::-1]

    elif operator == 'Insertion':
        # Select an index randomly to insert an SP
        insert_idx = np.random.randint(len(sol))
        # Select an SP randomly to insert
        sp_to_insert = np.random.choice(sol)
        # Insert the selected SP at the chosen index
        sol = np.insert(sol, insert_idx, sp_to_insert)

    return sol


# Example usage
sol = [35, 67, 6, 70, 75, 77, 52, 58]
new_sol = apply_operator(sol, 'Swap')
print("After Swap operation:", new_sol)

new_sol = apply_operator(sol, 'Reversion')
print("After Reversion operation:", new_sol)

new_sol = apply_operator(sol, 'Insertion')
print("After Insertion operation:", new_sol)
