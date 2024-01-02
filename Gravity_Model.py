## Developed by Sadra Daneshvar
### Feb 2, 2023

import numpy as np
import pandas as pd


def gravity_model(
    O,
    D,
    cost_matrix,
    deterrence_matrix,
    error_threshold=0.01,
    improvement_threshold=1e-4,
):
    def format_matrix(matrix, matrix_name):
        matrix_size = matrix.shape[0]
        column_names = [f"Zone {i}" for i in range(1, matrix_size + 1)]
        formatted_matrix = pd.DataFrame(
            matrix, columns=column_names, index=column_names
        )
        print(f"{matrix_name}:\n", formatted_matrix, "\n")

    # Print initial cost matrix and deterrence matrix
    format_matrix(cost_matrix, "Initial Cost Matrix")
    format_matrix(deterrence_matrix, "Deterrence Matrix")

    # Ensure the sum of O and D are equal
    sum_O = np.sum(O)
    sum_D = np.sum(D)
    if sum_O != sum_D:
        if sum_O < sum_D:
            correction_ratio = sum_D / sum_O
            O = O * correction_ratio
        else:
            correction_ratio = sum_O / sum_D
            D = D * correction_ratio

    n = len(O)  # Number of zones
    T = np.sum(O)  # Total number of trips

    # Initialize balancing factors
    Ai = np.ones(n)
    Bj = np.ones(n)

    previous_error = np.inf  # Set initial previous error to infinity
    iteration_count = 0
    stop_reason = ""

    while True:
        iteration_count += 1

        # Update Ai
        for i in range(n):
            Ai[i] = 1 / (np.sum(Bj * D * deterrence_matrix[i, :]) + 1e-9)

        # Update Bj
        Bj_new = np.ones(n)
        for j in range(n):
            Bj_new[j] = 1 / (np.sum(Ai * O * deterrence_matrix[:, j]) + 1e-9)

        # Calculate Tij
        Tij = np.outer(Ai * O, Bj_new * D) * deterrence_matrix

        # Calculate error
        error = (
            np.sum(np.abs(O - np.sum(Tij, axis=1)))
            + np.sum(np.abs(D - np.sum(Tij, axis=0)))
        ) / T

        # Calculate change in error
        error_change = abs(previous_error - error)

        # Check for convergence or slow improvement
        if error < error_threshold:
            stop_reason = "Error threshold met"
            break
        elif error_change < improvement_threshold:
            stop_reason = "Slow improvement"
            break

        previous_error = error  # Update previous error
        Bj = Bj_new

    # Generate column and row names and format final OD matrix
    final_matrix = pd.DataFrame(
        Tij,
        columns=[f"Zone {i}" for i in range(1, n + 1)],
        index=[f"Zone {i}" for i in range(1, n + 1)],
    )
    final_matrix["Origin"] = final_matrix.sum(axis=1)
    final_matrix.loc["Destination"] = final_matrix.sum()

    # Print final results
    print("Final OD Matrix:")
    print(final_matrix.round(3), "\n")
    print(f"Number of Iterations: {iteration_count}")
    print(f"Stopping Condition: {stop_reason}")
    print(f"Error: {error}")


# Set display options
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 100)
