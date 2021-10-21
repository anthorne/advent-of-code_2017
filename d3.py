import math

data = 265149
# data = 26


def print_data(dataset):
    for row in dataset:
        row_str = ''
        for col in row:
            row_str += str(col) + '\t'
        print(row_str)
    print('\n')


def new_direction(d):
    directions = ['e', 'n', 'w', 's']
    i = 0
    for di in directions:
        if di == d:
            n = i + 1
            if n > len(directions) - 1:
                n = 0
        i += 1
    return directions[n]


# create array
counter = 1
arraysize = round(math.sqrt(data)+1)
if arraysize % 2 == 0:
    arraysize += 1
p = [int((arraysize - 1) / 2), int((arraysize - 1) / 2)]
dataset = []
for x in range(arraysize):
    dataset.append([0])
    for y in range(arraysize - 1):
        dataset[x].append(0)
dataset[p[0]][p[1]] = counter
counter += 1


# fill array
direction = 'e'
step_len = 1
step_cnt = 0
step_even = False
for d in range(data - 1):
    # print('Number: ' + str(counter) + ' cur pos: ' + str(p) + ' dir: ' + str(direction) + ' steps: ' + str(step_len) + ' step counter: ' + str(step_cnt) + '\n')
    if direction == 'e':
        p = [p[0], p[1] + 1]
    elif direction == 'n':
        p = [p[0] - 1, p[1]]
    elif direction == 'w':
        p = [p[0], p[1] - 1]
    elif direction == 's':
        p = [p[0] + 1, p[1]]
    dataset[p[0]][p[1]] = counter
    counter += 1
    # print_data(dataset)
    step_len -= 1
    if step_len == 0:
        direction = new_direction(direction)
        if step_even:
            step_cnt += 1
            step_len = 1 + step_cnt
            step_even = False
        else:
            step_len = 1 + step_cnt
            step_even = True


# lookup value-position in array
r = 0
value_pos = [0, 0]
for row in dataset:
    c = 0
    for col in row:
        if col == data:
            value_pos = [r, c]
        c += 1
    r += 1
# print('Found value:' + str(data) + ' at position: [' + str(value_pos[0]) + '][' + str(value_pos[1]) + ']')


# count steps to origo
origo = int((len(dataset) + 1) / 2) - 1
# print('origo: ' + str(origo) + ' value: ' + str(dataset[origo][origo]))
x = value_pos[0] - origo
if x < 0:
    x = x * - 1
y = value_pos[1] - origo
if y < 0:
    y = y * - 1
steps_to_origo = x + y
# print(' x: ' + str(x) + ' y: ' + str(y))
print(' Part one - Number of steps is: ' + str(steps_to_origo))


# ------------ Part two -------------


def get_sum_of_adjecent(r, c):
    sum = 0
    r = r - 1
    c = c - 1
    c_origin = c
    for x in range(3):
        c = c_origin
        for y in range(3):
            sum += dataset[r][c]
            c += 1
        r += 1
    return sum


# create array
counter = 1
arraysize = round(math.sqrt(data)+1)
if arraysize % 2 == 0:
    arraysize += 1
p = [int((arraysize - 1) / 2), int((arraysize - 1) / 2)]
dataset = []
for x in range(arraysize):
    dataset.append([0])
    for y in range(arraysize - 1):
        dataset[x].append(0)
dataset[p[0]][p[1]] = counter
counter += 1


# fill array
direction = 'e'
step_len = 1
step_cnt = 0
step_even = False
break_next = False
part_two = 0
for d in range(data - 1):
    # print('Number: ' + str(counter) + ' cur pos: ' + str(p) + ' dir: ' + str(direction) + ' steps: ' + str(step_len) + ' step counter: ' + str(step_cnt) + '\n')
    if direction == 'e':
        p = [p[0], p[1] + 1]
    elif direction == 'n':
        p = [p[0] - 1, p[1]]
    elif direction == 'w':
        p = [p[0], p[1] - 1]
    elif direction == 's':
        p = [p[0] + 1, p[1]]
    counter = get_sum_of_adjecent(p[0], p[1])
    if counter > data:
        break_next = True
    dataset[p[0]][p[1]] = counter
    # print_data(dataset)
    if break_next:
        part_two = counter
        break
    step_len -= 1
    if step_len == 0:
        direction = new_direction(direction)
        if step_even:
            step_cnt += 1
            step_len = 1 + step_cnt
            step_even = False
        else:
            step_len = 1 + step_cnt
            step_even = True


print(' Part two - The next value is: ' + str(part_two))
