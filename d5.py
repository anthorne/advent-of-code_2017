file = open('d5_input.txt')
# file = open('d5_example.txt')

data = []
data2 = []

# Load data into array
for row in file:
    data.append([int(row.strip()), 0])
    data2.append([int(row.strip()), 0])
# Mark the current position
data[0][1] = 1
data2[0][1] = 1

num_entries = len(data)

def step_partone(data, entries):
    done = False
    # find current position
    steps_to_move = 0
    current_position = 0
    pos = 0
    for entry in data:
        if entry[1] == 1:
            # print('found stepper at pos: ' + str(pos))
            current_position = pos
            steps_to_move = entry[0]
        pos += 1

    # move position
    data[current_position][1] = 0
    data[current_position][0] += 1
    new_pos = current_position + steps_to_move
    if (new_pos + 1) > entries:
        done = True
    else:
        data[new_pos][1] = 1
    return data, done


def step_parttwo(data, entries):
    done = False
    # find current position
    steps_to_move = 0
    current_position = 0
    pos = 0
    for entry in data:
        if entry[1] == 1:
            # print('found stepper at pos: ' + str(pos))
            current_position = pos
            steps_to_move = entry[0]
        pos += 1

    # move position
    data[current_position][1] = 0
    if steps_to_move >= 3:
        data[current_position][0] -= 1
    else:
        data[current_position][0] += 1
    new_pos = current_position + steps_to_move
    if (new_pos + 1) > entries:
        done = True
    else:
        data[new_pos][1] = 1
    return data, done


num_steps = 0
finished = False
# print(data)
while not finished:
    num_steps += 1
    process = step_partone(data, num_entries)
    finished = process[1]
    data = process[0]
    # print(data)

print(' Part one: It took ' + str(num_steps) + ' steps to finish!')

num_steps = 0
finished = False
# print(data2)
while not finished:
    num_steps += 1
    process = step_parttwo(data2, num_entries)
    finished = process[1]
    data2 = process[0]
    # print(data2)

print(' Part two: It took ' + str(num_steps) + ' steps to finish!')
