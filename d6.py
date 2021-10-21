# Advent of code - day 6

data = [11, 11, 13, 7, 0, 15, 5, 5, 4, 4, 1, 1, 7, 1, 15, 11]
# data = [0, 2, 7, 0]


# find memory bank with most blocks - returns [position, value]
def find_memorybank(data_memory):
    pos = 0
    blocks = 0
    counter = 0
    for i in data_memory:
        if i > blocks:
            blocks = i
            pos = counter
        counter += 1
    return pos, blocks


def redistribute(data_mem):
    pos, blocks = find_memorybank(data_mem)
    data_mem[pos] = 0
    memorybanks = len(data_mem) - 1
    current_pos = pos
    for i in range(blocks):
        if current_pos + 1 > memorybanks:
            current_pos = 0
        else:
            current_pos += 1
        data_mem[current_pos] += 1
    return data_mem


# start memory redistribution and break when loop is found!
positions = list()
positions.append(data.copy())
no_duplicates = True
redistributions = 0
while no_duplicates:
    new_position = redistribute(data).copy()
    redistributions += 1
    for pos in positions:
        if pos == new_position:
            no_duplicates = False
            break
    positions.append(new_position)


# get the size of the loop
loop_content = positions[-1].copy()
counter = 0
for p in positions:
    if p == loop_content:
        break
    counter += 1
loop_size = len(positions) - 1 - counter


# print(str(positions))
print(' Part one - Number of redistributions when duplicate found: ' + str(redistributions))
print(' Part two - Loop size: ' + str(loop_size))

