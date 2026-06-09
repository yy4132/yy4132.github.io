import numpy as np
import pandas as pd
from datetime import datetime

sudoku = pd.read_csv("sudoku.csv\sudoku.csv")
sample = sudoku.loc[2020]

def decode_sudoku(sample: str) -> np.matrix:
    return np.matrix([np.array(list(sample[i:i+9])).astype(np.int64) for i in range(0, len(sample), 9)])

decoded_puzzle = decode_sudoku(sample['puzzle'])
decoded_puzzle

def encode_sudoku(sudoku: np.matrix) -> str:
    return ''.join([''.join(list(r.astype(str))) for r in np.asarray(sudoku)])

encoded_puzzle = encode_sudoku(decoded_puzzle)

assert encoded_puzzle == sample['puzzle']
encoded_puzzle

from ortools.sat.python import cp_model

def solve_with_cp(grid: np.matrix) -> (np.matrix, float):
    assert grid.shape == (9,9)
    grid_size = 9
    region_size = 3
    model = cp_model.CpModel()
    x = {}
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] != 0:
                x[i, j] = grid[i, j]
            else:
                x[i, j] = model.NewIntVar(1, grid_size, 'x[{},{}]'.format(i,j) )
    for i in range(grid_size):
        model.AddAllDifferent([x[i, j] for j in range(grid_size)])
    for j in range(grid_size):
        model.AddAllDifferent([x[i, j] for i in range(grid_size)])
    for row_idx in range(0, grid_size, region_size):
        for col_idx in range(0, grid_size, region_size):
            model.AddAllDifferent([x[row_idx + i, j] for j in range(col_idx, (col_idx + region_size)) for i in range(region_size)])
    solver = cp_model.CpSolver()
    start = datetime.now()
    status = solver.Solve(model)
    exec_time = datetime.now() - start
    result = np.zeros((grid_size, grid_size)).astype(np.int64)
    if status == cp_model.FEASIBLE:
        for i in range(grid_size):
            for j in range(grid_size):
                result[i,j] = int(solver.Value(x[i,j]))
    else:
        raise Exception('Unfeasible Sudoku')
    return result, exec_time.total_seconds()
    res, _ = solve_with_cp(decoded_puzzle)
    cp_solution = encode_sudoku(res) 
    assert cp_solution == sample['solution']
    res

from ortools.linear_solver import pywraplp

def solve_with_ip(grid: np.ndarray) -> (np.ndarray, float):
    assert grid.shape == (9,9)
    grid_size = 9
    cell_size = 3
    solver = pywraplp.Solver('Sudoku Solver', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    x = {}
    for i in range(grid_size):
        for j in range(grid_size):
            for k in range(grid_size):
                x[i, j, k] = solver.BoolVar('x[%i,%i,%i]' % (i, j, k))
    for i in range(grid_size):
        for j in range(grid_size):
            defined = grid[i, j] != 0
            if defined:
                solver.Add(x[i,j,grid[i, j]-1] == 1)
    for i in range(grid_size):
        for j in range(grid_size):
            solver.Add(solver.Sum([x[i, j, k] for k in range(grid_size)]) == 1)
    for k in range(grid_size):
        for i in range(grid_size):
            solver.Add(solver.Sum([x[i, j, k] for j in range(grid_size)]) == 1)
        for j in range(grid_size):
            solver.Add(solver.Sum([x[i, j, k] for i in range(grid_size)]) == 1)
        for row_idx in range(0, grid_size, cell_size):
            for col_idx in range(0, grid_size, cell_size):
                solver.Add(solver.Sum([x[row_idx + i, j, k] for j in range(col_idx, (col_idx + cell_size)) for i in range(cell_size)]) == 1)
    start = datetime.now()
    status = solver.Solve()
    exec_time = datetime.now() - start
    statusdict = {0:'OPTIMAL', 1:'FEASIBLE', 2:'INFEASIBLE', 3:'UNBOUNDED', 4:'ABNORMAL', 5:'MODEL_INVALID', 6:'NOT_SOLVED'}
    result = np.zeros((grid_size, grid_size)).astype(np.int64)
    if status == pywraplp.Solver.OPTIMAL:
        for i in range(grid_size):
            for j in range(grid_size):
                result[i,j] = sum((k + 1) * int(x[i, j, k].solution_value()) for k in range(grid_size))
    else:
        raise Exception('Unfeasible Sudoku: {}'.format(statusdict[status]))
    return result, exec_time.total_seconds()
res, _ = solve_with_ip(decoded_puzzle)
ip_solution = encode_sudoku(res) 
assert ip_solution == sample['solution']
res

def solve_sudoku(instance: np.matrix, solver: str = 'ip') -> (np.matrix, float):
    if solver == 'ip':
        return solve_with_ip(instance)
    elif solver == 'cp':
        return solve_with_cp(instance)
    else:
        raise Exception('Unknown solver: {}'.format(solver))

solve_sudoku(decode_sudoku(sample['puzzle']))

from tqdm.notebook import tqdm

sample_size = 1000
seed = 2020
ip_exec_time = []
cp_exec_time = []

for index, row in tqdm(sudoku.sample(sample_size, random_state=seed).iterrows()):
    res, exec_time = solve_sudoku(decode_sudoku(row.puzzle), 'cp')
    assert encode_sudoku(res) == row.solution
    cp_exec_time += [exec_time]
    res, exec_time = solve_sudoku(decode_sudoku(row.puzzle), 'ip')
    assert encode_sudoku(res) == row.solution
    ip_exec_time += [exec_time]

performance_df = pd.DataFrame({'IP' : ip_exec_time, 'CP' : cp_exec_time})
performance_df.head()