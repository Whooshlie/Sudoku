import copy
import random

TRY = 50


def possible_value(i: int, sudoku: list[list[int]]):
    poss = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    x = i // 9
    y = i % 9
    for i in range(0, 9):
        if sudoku[x][i] in poss:
            poss.remove(sudoku[x][i])
        if sudoku[i][y] in poss:
            poss.remove(sudoku[i][y])

    square = (x // 3, y // 3)
    for i in range(0, 3):
        x_check = square[0] * 3 + i
        for j in range(0, 3):
            y_check = square[1] * 3 + j
            if sudoku[x_check][y_check] in poss:
                poss.remove(sudoku[x_check][y_check])
    return poss


def generate_full_recur(i: int, sudoku: list[list[int]]):
    if i == 81:
        return True, sudoku

    x = i // 9
    y = i % 9
    poss = possible_value(i, sudoku)

    if len(poss) == 0:
        return False, sudoku

    for j in range(len(poss)):
        curr = random.choice(tuple(poss))
        poss.remove(curr)
        sudoku_curr = copy.deepcopy(sudoku)
        sudoku_curr[x][y] = curr
        res, out = generate_full_recur(i + 1, sudoku_curr)
        if res:
            return True, out

    return False, sudoku


def generate_full():
    sudoku = [[0] * 9 for x in range(0, 9)]
    return generate_full_recur(0, sudoku)[1]


def check_solution_recur(i: int, sudoku: list[list[int]], num):
    x = i // 9
    y = i % 9

    if num[0] > 1:
        return 0

    if i == 81:
        num[0] += 1
        return 1

    while sudoku[x][y] != 0:
        i = i + 1
        x = i // 9
        y = i % 9
        if i == 81:
            return 1

    out = 0
    poss = possible_value(i, sudoku)
    poss = list(poss)
    for j in range(len(poss)):
        sudoku_curr = copy.deepcopy(sudoku)
        sudoku_curr[x][y] = poss[j]
        out += check_solution_recur(j + 1, sudoku_curr, num)
    return out


def have_unique_solution(sudoku: list[list[int]]):
    return check_solution_recur(0, sudoku, [0]) == 1


def generate_sudoku():
    sudoku = generate_full()
    check = list(range(0, 81))
    random.shuffle(check)
    test = 0
    for j, i in enumerate(check[0:TRY]):
        x = i // 9
        y = i % 9
        c = sudoku[x][y]
        sudoku[x][y] = 0

        if a := not have_unique_solution(sudoku):
            sudoku[x][y] = c
        else:
            test += 1
        print(a, j)
    print(test)
    return sudoku
