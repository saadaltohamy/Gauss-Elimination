import numpy as np
import config
from flask import redirect, render_template, request, session

first_rec = True
rows = 1
cols = 1


def row_echelon(A):
    global first_rec
    global rows
    global cols
    """ Return Row Echelon Form of matrix A """

    # if matrix A has no columns or rows,
    # it is already in REF, so we return itself
    r, c = A.shape
    if r == 0 or c == 0:
        return A

    # we search for non-zero element in the first column
    for i in range(len(A)):
        if A[i,0] != 0:
            break
    else:
        # if all elements in the first column is zero,
        # we perform REF on matrix from second column
        B = row_echelon(A[:,1:])
        # and then add the first zero-column back
        A = np.hstack([A[:,:1], B])
        print(A)
        print_steps(A)
        return A

    # if non-zero element happens not in the first row,
    # we switch rows
    if i > 0:
        print(f"Swap the row {rows} with row{rows + i}")
        s = f"Swap the row {rows} with row{rows + i}"
        config.steps.append(s)
        ith_row = A[i].copy()
        A[i] = A[0]
        A[0] = ith_row
        print_steps(A)

    # we divide first row by first element in it
    print(f"Make the pivot in the row{rows} by dividing the row{rows} by {A[0,0]}")
    s = f"Make the pivot in the row{rows} by dividing the row{rows} by {A[0,0]}"
    config.steps.append(s)
    A[0] = A[0] / A[0, 0]
    A += 0   # To discard -0.0
    print_steps(A)

    # we subtract all subsequent rows with first row (it has 1 now as first element)
    # multiplied by the corresponding element in the first column
    print(f"Eliminate the column{cols}")
    s = f"Eliminate the column{cols}"
    config.steps.append(s)

    A[1:] -= A[0] * A[1:,0:1]
    A += 0  # To discard -0.0

    print_steps(A)
    cols += 1
    rows +=1
    # we perform REF on matrix from second row, from second column
    B = row_echelon(A[1:,1:])
    # we add first row and first (zero) column, and return
    A = np.vstack([A[:1], np.hstack([A[1:,:1], B]) ])
    return A


def print_steps(arr):
    global first_rec
    if first_rec:
        first_rec = False
        r, c = arr.shape
        config.step = np.zeros([r, c], dtype=float)
        config.step = arr
        print(config.step)
        b = np.copy(config.step)
        config.steps.append(b)

    else:
        r, c = arr.shape
        r1, c1 = config.step.shape
        row_changing = r1 - r
        config.step[row_changing:, row_changing:] = arr
        print(config.step)
        b = np.copy(config.step)
        config.steps.append(b)
        print("")
