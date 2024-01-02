## Developed by Sadra Daneshvar
### Feb 2, 2023

import numpy as np  # Import numpy for numerical operations
import pandas as pd  # Import pandas for data manipulation


# Define a function named 'gravity_model'
def gravity_model(
    O,  # Origin matrix
    D,  # Destination matrix
    cost_matrix,  # Cost matrix
    deterrence_matrix,  # Deterrence matrix
    error_threshold=0.01,  # Error threshold for stopping condition
    improvement_threshold=1e-4,  # Improvement threshold for stopping condition
):
    # Define a nested function to format and print matrices
    def format_matrix(matrix, matrix_name):
        matrix_size = matrix.shape[0]  # Get the number of rows in the matrix
        # Create column names for the matrix
        column_names = [f"Zone {i}" for i in range(1, matrix_size + 1)]
        # Convert the matrix into a pandas DataFrame for pretty printing
        formatted_matrix = pd.DataFrame(
            matrix, columns=column_names, index=column_names
        )
        # Print the formatted matrix
        print(f"{matrix_name}:\n", formatted_matrix, "\n")

    # Print the initial cost matrix and deterrence matrix
    format_matrix(cost_matrix, "Initial Cost Matrix")
    format_matrix(deterrence_matrix, "Deterrence Matrix")

    # Normalize O and D so their sums are equal
    sum_O = np.sum(O)  # Sum of all elements in O
    sum_D = np.sum(D)  # Sum of all elements in D
    # Adjust O or D if their sums are not equal
    if sum_O != sum_D:
        if sum_O < sum_D:
            correction_ratio = sum_D / sum_O  # Calculate correction ratio
            O = O * correction_ratio  # Adjust O by the correction ratio
        else:
            correction_ratio = sum_O / sum_D  # Calculate correction ratio
            D = D * correction_ratio  # Adjust D by the correction ratio

    n = len(O)  # Number of zones
    T = np.sum(O)  # Total number of trips

    # Initialize balancing factors Ai and Bj
    Ai = np.ones(n)  # Ai balancing factor, initially set to 1 for each zone
    Bj = np.ones(n)  # Bj balancing factor, initially set to 1 for each zone

    previous_error = np.inf  # Initialize previous error to infinity
    iteration_count = 0  # Initialize iteration count
    stop_reason = ""  # Initialize stop reason string

    # Iterative process
    while True:
        iteration_count += 1  # Increment iteration count

        # Update Ai balancing factors
        for i in range(n):
            Ai[i] = 1 / (np.sum(Bj * D * deterrence_matrix[i, :]) + 1e-9)

        # Update Bj balancing factors
        Bj_new = np.ones(n)  # Temporary array for new Bj values
        for j in range(n):
            Bj_new[j] = 1 / (np.sum(Ai * O * deterrence_matrix[:, j]) + 1e-9)

        # Calculate Tij matrix for the model
        Tij = np.outer(Ai * O, Bj_new * D) * deterrence_matrix

        # Calculate the error of the model
        error = (
            np.sum(np.abs(O - np.sum(Tij, axis=1)))
            + np.sum(np.abs(D - np.sum(Tij, axis=0)))
        ) / T

        # Calculate the change in error from the previous iteration
        error_change = abs(previous_error - error)

        # Check stopping conditions
        if error < error_threshold:
            stop_reason = "Error threshold met"  # Set stop reason
            break  # Break the loop if error threshold is met
        elif error_change < improvement_threshold:
            stop_reason = "Slow improvement"  # Set stop reason
            break  # Break the loop if improvement is slow

        previous_error = error  # Update the previous error
        Bj = Bj_new  # Update Bj with new values

    # Format and print the final OD matrix
    final_matrix = pd.DataFrame(
        Tij,
        columns=[f"Zone {i}" for i in range(1, n + 1)],
        index=[f"Zone {i}" for i in range(1, n + 1)],
    )
    final_matrix["Origin"] = final_matrix.sum(axis=1)  # Add sum of rows as Origin
    final_matrix.loc[
        "Destination"
    ] = final_matrix.sum()  # Add sum of columns as Destination

    # Print the final results
    print("Final OD Matrix:")
    print(
        final_matrix.round(3), "\n"
    )  # Print the final OD matrix rounded to 3 decimal places
    print(f"Number of Iterations: {iteration_count}")  # Print the number of iterations
    print(f"Stopping Condition: {stop_reason}")  # Print the stopping condition
    print(
        f"Error: {error*100:.3f}%"
    )  # Print the final error as a percentage with 3 decimal places
