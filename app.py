import config
import numpy as np
import methods
from methods import row_echelon
from flask import Flask, render_template, request

# Configure application
app = Flask(__name__)

rows = 0
cols = 0
A = np.zeros([rows,cols], dtype=float)
@app.route('/', methods=["GET", "POST"])
def index():
    global rows
    global cols
    # Assign row and cols from input user
    if request.method == "POST":
        rows = int(request.form.get("equations"))
        cols = int(request.form.get("variables")) + 1
        return render_template("matrix.html", rows=rows, cols=cols)
    else:
        return render_template("index.html")


@app.route('/add_matrix', methods=["GET", "POST"])
def matrix():
    global rows
    global cols
    global A

    # Return all variables to default
    A = np.zeros([rows,cols], dtype=float)
    methods.rows = 1
    methods.cols = 1
    methods.first_rec = True
    config.step = np.zeros([rows, cols], dtype=float)
    config.steps = []
    config.solutions = []

    # Assign the Array from the user
    for i in range(rows):
        for j in range(cols):
            A[i, j] = float(request.form.get(f"r{i}_c{j}"))
    return render_template("confirm.html", A=A, rows=rows, cols=cols)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        return render_template("edit.html", A=A, rows=rows, cols=cols)


@app.route("/solution", methods=["GET", "POST"])
def solution():
    global rows
    global cols
    global A

    print("Your Matrix")
    s = "Your Matrix"
    config.steps.append(s)
    print(A)
    config.steps.append(A)

    # check if there are any zero rows and delete it
    zero_rows = np.all((A == 0), axis=1)  # True or False
    A = A[~np.all(A == 0, axis=1)]
    zero_cols = np.all((A == 0), axis=0)  # True or False
    r, c = A.shape
    print(r)
    print(c)
    if np.any(zero_rows):
        print("Your Matrix without zero rows")
        s = "Your Matrix without zero rows"
        config.steps.append(s)
        print(A)
        config.steps.append(A)

    if np.any(zero_cols):
        A = A[:, ~np.all(A == 0, axis=0)]
        print("Your Matrix without zero columns")
        s = "Your Matrix without zero columns"
        config.steps.append(s)
        print(A)
        config.steps.append(A)
    r, c = A.shape

    if r == 1:
        print("System is inconsistent")
        s = "System is inconsistent"
        config.solutions.append(s)
        print("Please add more than one row")
        s = "Please add more than one row"
        config.solutions.append(s)
        return render_template("solutions.html", steps=config.steps, solutions=config.solutions, cols=cols,
                               rows=rows)
    if c < 3:
        print("System is inconsistent")
        s = "System is inconsistent"
        config.solutions.append(s)
        print("Please add two variables or more")
        s = "Please add two variables or more"
        config.solutions.append(s)
        return render_template("solutions.html", steps=config.steps, solutions=config.solutions, cols=c,
                               rows=r)

    if r == c - 1:  # Number of equations = number of variables
        row_echelon(A)

        # Separation process
        c = c - 1    # columns starting with 0 not 1
        b = np.array(A[0, c])
        for i in range(1, r):
            b = np.hstack([b, A[i, c]])
        A = np.delete(A, c, axis=1)
        n = len(b)

        # calculate the determinant and check if it is equal to zero
        if np.linalg.det(A) == 0:
            print("System is inconsistent")
            s = "System is inconsistent"
            config.solutions.append(s)
            return render_template("solutions.html", steps=config.steps, solutions=config.solutions, cols=cols, rows=rows)

        # Back_Substitutions
        x = np.zeros(n, float)  # solutions
        n = n - 1  # length of elements in right side((b) number of equations) starting with 0 (not 1)
        x[n] = b[n]
        for i in range(n - 1, -1, -1):
            sum_ax = 0
            for j in range(i + 1, n + 1):
                sum_ax += A[i, j] * x[j]
            x[i] = (b[i] - sum_ax)

        # print solutions
        print("Solutions")
        s = "Solutions"
        config.solutions.append(s)
        for i in range(n + 1):
            print(f"x{i + 1} = {x[i]}")
            s = f"x{i + 1} = {x[i]}"
            config.solutions.append(s)
        c = c + 1
    elif r > c - 1:  # Number of equations > number of variables
        print(r)
        print(c)
        row_echelon(A)
        print("System is inconsistent")
        s = "System is inconsistent"
        config.solutions.append(s)
    elif r < c - 1:  # Number of equations < number of variables
        row_echelon(A)
        print("infinity solutions")
        s = "infinity solutions"
        config.solutions.append(s)
    print(f"columns: {c}")
    return render_template("solutions.html", steps=config.steps, solutions=config.solutions, cols=c, rows=r)

