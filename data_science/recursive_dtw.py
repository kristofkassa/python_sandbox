import numpy as np


def dtw(x, y, c_o, c_ny, i, j):
    if i == 0 and j == 0:
        return abs(x[i] - y[i])
    elif i == 0:
        return abs(x[i] - y[i]) + dtw(x, y, c_o, c_ny, i, j - 1) + c_o
    elif j == 0:
        return abs(x[i] - y[i]) + dtw(x, y, c_o, c_ny, i - 1, j) + c_ny
    else:
        return abs(x[i] - y[i]) + min(dtw(x, y, c_o, c_ny, i - 1, j) + c_ny, dtw(x, y, c_o, c_ny, i, j - 1) + c_o,
                                      dtw(x, y, c_o, c_ny, i - 1, j - 1))


def dtw2(x, y, c_o, c_ny, i, j, table=None):
    if table is None:
        table = np.zeros([x.size, y.size], dtype=int)

    if table[i][j] != 0:
        return table[i][j]
    else:
        if i == 0 and j == 0:
            return abs(x[i] - y[i])
        elif i == 0:
            table[i][j] = abs(x[i] - y[i]) + dtw2(x, y, c_o, c_ny, i, j - 1, table) + c_o
            return table[i][j]
        elif j == 0:
            table[i][j] = abs(x[i] - y[i]) + dtw2(x, y, c_o, c_ny, i - 1, j, table) + c_ny
            return table[i][j]
        else:
            table[i][j] = abs(x[i] - y[i]) + min(dtw2(x, y, c_o, c_ny, i - 1, j, table) + c_ny,
                                                 dtw2(x, y, c_o, c_ny, i, j - 1, table) + c_o,
                                                 dtw2(x, y, c_o, c_ny, i - 1, j - 1, table))
            return table[i][j]


def route(input_table):
    route_table = np.zeros([input_table.shape[0], input_table.shape[1]], dtype=int)

    route_found = False
    i = j = input_table.shape[0]-1
    while not route_found:

        # print(i, j)

        if i == j == 0:
            route_table[i][j] = 1
            return route_table

        route_table[i][j] = 1

        neighbours = {
             1: input_table[i-1][j],
             2: input_table[i][j-1],
             3: input_table[i-1][j-1],
        }

        # print(neighbours)
        # print(min(neighbours, key=neighbours.get))

        next_step = min(neighbours, key=neighbours.get)
        if next_step == 1:
            i -= 1
        elif next_step == 2:
            j -= 1
        else:
            i -= 1
            j -= 1


def main():
    series_1 = np.random.randint(1, 100, 10)
    series_2 = np.random.randint(1, 100, 10)

    print(series_1, series_2)
    result1 = dtw(series_1, series_2, 1, 1, 9, 9)
    result2 = dtw2(series_1, series_2, 1, 1, 9, 9)

    print(result1, result2)

    table = np.array([[0,35,53,71,89,107,125,143,161,179],
                [24,23,30,37,44,51,58,65,72,79],
                [101,100,99,106,113,120,127,134,141,148],
                [129,128,127,126,133,140,147,154,161,168],
                [164,163,162,161,160,167,174,181,188,195],
                [232,231,230,229,228,227,234,241,248,255],
                [277,276,275,274,273,272,271,278,285,292],
                [293,292,291,290,289,288,287,286,293,300],
                [318,317,316,315,314,313,312,311,310,309],
                [329,328,327,326,325,324,323,322,321,320]])

    print(table)

    print(route(table))


if __name__ == '__main__':
    main()
