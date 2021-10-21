# Advent of Code - 2017 - day 14 - Pure Knot Hash Function

# Create a representation of the memory
def create_memory_block(mem_size):
    memory = list()
    pos = 0
    state = 'x'                       # current states : 'x' = current position , '' = inactive , 's' = selected
    for i in range(mem_size):
        if i > 0:
            state = ''
        pos += 1
        memory.append([i, [0, 0, 0, 0], state])
    return memory


def get_current_position(memory):
    pos = int()
    count = 0
    for m in memory:
        if m[2] == 'x':
            pos = count
            break
        count += 1
    return pos


def set_current_position(memory, cur_pos):
    for m in memory:
        if m[2] == 'x':
            m[2] = ''
            break
    count = 0
    for m in memory:
        if count == cur_pos:
            m[2] = 'x'
            break
        count += 1
    return memory


def unselect_memory(memory):
    for y in memory:
        if y[2] == 's':
            y[2] = ''
    return memory


def select_memory(memory, selection_len):
    # clear old selection
    memory = unselect_memory(memory)
    # select new
    current_pos = int()
    count = 0
    for i in memory:
        if i[2] == 'x':
            current_pos = count
        count += 1
    mem_len = len(memory) - 1
    counter = current_pos + 1
    for x in range(selection_len - 1):
        if counter > mem_len:
            counter = 0
        if memory[counter][2] == 'x':
            print('error!! the selection is bigger than the memory itself! - debug: ' + str(memory))
        memory[counter][2] = 's'
        counter += 1
    return memory


def reverse_selected_memory(memory):
    mem_values = list()
    mem_positions = list()
    start_pos = int()
    x_found = False
    order = 0
    pos = 0
    # look for the beginning of selection = 'x'
    for m in memory:
        if m[2] == 'x':
            mem_values.append(m[0])                     # memory values
            mem_positions.append([order, pos])          # memory position
            start_pos = pos
            x_found = True
        if x_found and m[2] == 's':
            mem_values.append(m[0])                     # memory values
            mem_positions.append([order, pos])          # memory position
        order += 1
        pos += 1
    pos = 0
    # get the rest of the selected values if any in a second iteration
    for m in memory:
        if pos == start_pos:
            break
        else:
            if m[2] == 's' or m[2] == 'x':
                mem_values.append(m[0])                     # memory values
                mem_positions.append([order, pos])          # memory position
        order += 1
        pos += 1
    mem_positions.sort(reverse=True)
    v = 0
    for p in mem_positions:
        p2 = p[1]
        memory[p2][0] = mem_values[v]
        v += 1
    return memory


def perform_selection(memory, step, input_lenghts):
    # get selection length
    selection_len = -1
    if len(input_lenghts[0]) > step:
        selection_len = input_lenghts[0][step]
    else:
        return memory, -1
    step += 1

    # select the memory
    memory = select_memory(memory, selection_len)
    return memory, step


def move_current_position(memory, step, skip_size, input_lenghts):
    steps = input_lenghts[0][step]
    old_pos = int()
    counter = 0
    for m in memory:
        if m[2] == 'x':
            old_pos = counter
            m[2] = ''
            break
        counter += 1
    new_pos = old_pos + steps + skip_size
    while len(memory) <= new_pos:
        new_pos = new_pos - len(memory)
    memory[new_pos][2] = 'x'
    return memory


def run(skip_size, memory, input_lenghts):
    # Init variables
    running = True
    step = 0
    program_cycle = 0

    while running:
        # First cycle
        if program_cycle == 0:
            program_cycle += 1

        # Get instruction
        elif program_cycle == 1:
            program_cycle += 1

        # Select the memory blocks
        elif program_cycle == 2:
            memory, step = perform_selection(memory, step, input_lenghts)
            if step == -1:
                running = False
            program_cycle += 1

        # Reverse selected memory
        elif program_cycle == 3:
            memory = reverse_selected_memory(memory)
            program_cycle += 1

        # Unselect memory
        elif program_cycle == 4:
            memory = unselect_memory(memory)
            program_cycle += 1

        # Move current position by the selection length + skip_size
        elif program_cycle == 5:
            memory = move_current_position(memory, step - 1, skip_size, input_lenghts)
            program_cycle += 1

        # Increase skip_size by +1
        elif program_cycle == 6:
            skip_size += 1
            program_cycle = 1

    current_position = get_current_position(memory)
    return skip_size, memory


def knot(input_part2):
    # variables
    skip_size = 0
    mem_size = 256

    # ---- PART TWO ----
    part2_suffix = [17, 31, 73, 47, 23]
    input_part2_ascii = [[]]
    for c in input_part2:
        input_part2_ascii[0].append(ord(c))

    # add the suffix to the input lengths
    for s in part2_suffix:
        input_part2_ascii[0].append(s)

    # reset the memory
    memory = create_memory_block(mem_size)

    input_lenghts = input_part2_ascii
    for r in range(64):
        skip_size, memory = run(skip_size, memory, input_lenghts)

    # create the dense hash
    sparse_hash = list()
    dense_hash = list()
    sparse_hash_len = 16
    char_count = 1
    hash_row = list()
    for c in range(len(memory)):
        hash_row.append(memory[c][0])
        if char_count == sparse_hash_len:
            sparse_hash.append(hash_row)
            hash_row = list()
            char_count = 0
        char_count += 1
    if len(hash_row) != 0:
        print('now what?!')
    # print(sparse_hash)
    # perform bitewise XOR
    for block in sparse_hash:
        result = 0
        first_round = True
        for c in block:
            if first_round:
                result = c
                first_round = False
            else:
                result = result ^ c
        dense_hash.append(result)
    # print(dense_hash)
    # convert to hex-values
    dense_hash_hex = str()
    for v in dense_hash:
        h = str(hex(v)).split('x')[1]
        if len(h) == 1:
            h = '0' + h
        dense_hash_hex += h
    # print(' Part two - The dense hash is: ' + str(dense_hash_hex))
    return dense_hash_hex

# # TESTING
#
# # input data
# input_part2 = '192,69,168,160,78,1,166,28,0,83,198,2,254,255,41,12'
# input_part2 = 'AoC 2017'
#
#
# dense_hash_hex = knot(input_part2)
# if '33efeb34ea91902bb2f59c9920caa6cd' == dense_hash_hex:
#     print('  ---->>>  !!! MATCHING HASHES - IT WORKS !!!  <<<----')
#
