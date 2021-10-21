# Advent of Code - 2017 - day 10
import pygame

# Initialize the game engine
pygame.init()
pygame.display.set_caption('anthorne - Advent of Code')
size = [800, 600]
screen = pygame.display.set_mode(size)

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (128, 128, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Define fonts
pygame.font.init()
font = pygame.font.SysFont('liberationmono', 10, bold=False)
font2 = pygame.font.SysFont('liberationmono', 20, bold=False)
font3 = pygame.font.SysFont('liberationmono', 15, bold=False)

header_text = font2.render('Advent of Code - day 10 - part 1 (anthorne)', True, WHITE)
screen.blit(header_text, (105, 15))

# input data
skip_size = 0
example_data = False
circular_list = list()
input_lenghts = list()
if example_data:
    input_lenghts.append([3, 4, 1, 5])  # example data
    circular_list.append([0, 1, 2, 3, 4])  # example data
    input_part2 = '3,4,1,5'
else:
    input_lenghts.append([192, 69, 168, 160, 78, 1, 166, 28, 0, 83, 198, 2, 254, 255, 41, 12])
    input_part2 = '192,69,168,160,78,1,166,28,0,83,198,2,254,255,41,12'
    circular_list.append([])
    for i in range(256):
        circular_list[0].append(int(i))


# Create a representation of the memory
def create_memory_block(mem_size):
    memory = list()
    padding_top = 40
    padding_sides = 100
    block_size = 25
    row_count = 1
    pos = 0
    state = 'x'                       # current states : 'x' = current position , '' = inactive , 's' = selected
    for i in range(mem_size):
        if i > 0:
            state = ''
        pos += 1
        if (pos * block_size) + (padding_sides * 2) > size[0]:
            padding_top += block_size
            row_count += 1
            pos = 1
        a = [padding_sides + (block_size * pos) - block_size, padding_top]
        b = [padding_sides + (block_size * pos), padding_top]
        c = [padding_sides + (block_size * pos), padding_top + block_size]
        d = [padding_sides + (block_size * pos) - block_size, padding_top + block_size]
        memory.append([i, [a, b, c, d], state])
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
    return


# Draw the representation of the memory
def draw_memory(memory):
    for i in memory:
        a = i[1][0]
        b = i[1][1]
        c = i[1][2]
        d = i[1][3]

        state = i[2]
        text_color = GRAY
        bg_color = BLACK
        if state == 'x':
            text_color = WHITE
            bg_color = YELLOW
        if state == 's':
            text_color = WHITE
            bg_color = GREEN

        # fill the background
        pygame.draw.rect(screen, bg_color, (a[0], a[1], b[0] - a[0], b[0] - a[0]))

        # write the text
        mem_text = font.render(str(i[0]), False, text_color)
        screen.blit(mem_text, (a[0] + 4, a[1] + 2))

        # draw the lines
        pygame.draw.line(screen, GRAY, a, b)
        pygame.draw.line(screen, GRAY, b, c)
        pygame.draw.line(screen, GRAY, c, d)
        pygame.draw.line(screen, GRAY, d, a)
    return


def set_status_position(memory):
    position = [800, 0]
    for i in memory:
        if i[1][3][1] > position[1]:
            position[1] = i[1][3][1]
        if i[1][3][0] < position[0]:
            position[0] = i[1][3][0]
    position[1] = position[1] + 3
    return position


def unselect_memory(memory):
    for y in memory:
        if y[2] == 's':
            y[2] = ''


def select_memory(memory, selection_len):
    # clear old selection
    unselect_memory(memory)
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


def perform_selection(memory, step):
    # get selection length
    selection_len = -1
    if len(input_lenghts[0]) > step:
        selection_len = input_lenghts[0][step]
    else:
        return -1
    step += 1
    if selection_len != -1:
        pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 500, 50))
        status_text = font3.render('The selection lenght is: ' + str(selection_len), True, WHITE)
        screen.blit(status_text, status_position)

    # select the memory
    select_memory(memory, selection_len)
    return step


def move_current_position(memory, step, skip_size):
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


def run(input_lenghts, skip_size, speed):
    # Init variables
    running = True
    clock = pygame.time.Clock()
    step = 0
    program_cycle = 0

    while running:
        # This limits the while loop to x times per second.
        clock.tick(speed)

        # check if the user clicked close
        for event in pygame.event.get():    # User did something
            if event.type == pygame.QUIT:   # If user clicked close
                pygame.quit()               # Flag that we are done so we exit this loop

        # First cycle
        if program_cycle == 0:
            pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
            status_text = font3.render('Instructions: ' + str(input_lenghts), True, WHITE)
            screen.blit(status_text, status_position)
            program_cycle += 1

        # Get instruction
        elif program_cycle == 1:
            pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
            if step < len(input_lenghts[0]):
                status_text = font3.render('Performing current instruction: ' + str(input_lenghts[0][step]), True, WHITE)
                screen.blit(status_text, status_position)
            program_cycle += 1

        # Select the memory blocks
        elif program_cycle == 2:
            step = perform_selection(memory, step)
            if step == -1:
                running = False
            pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
            status_text = font3.render('Performing current instruction: ' + str(input_lenghts[0][step - 1]) + ' - Memory selected!', True, WHITE)
            screen.blit(status_text, status_position)
            program_cycle += 1

        # Reverse selected memory
        elif program_cycle == 3:
            reverse_selected_memory(memory)
            pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
            status_text = font3.render('Performing current instruction: ' + str(input_lenghts[0][step - 1]) + ' - Selected memory is reversed!', True, WHITE)
            screen.blit(status_text, status_position)
            program_cycle += 1

        # Unselect memory
        elif program_cycle == 4:
            unselect_memory(memory)
            pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
            program_cycle += 1

        # Move current posision by the selection lenght + skip_size
        elif program_cycle == 5:
            move_current_position(memory, step - 1, skip_size)
            pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
            status_text = font3.render('Moving to new position!', True, WHITE)
            screen.blit(status_text, status_position)
            program_cycle += 1

        # Increase skip_size by +1
        elif program_cycle == 6:
            skip_size += 1
            pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
            status_text = font3.render('Skip size is now increased!', True, WHITE)
            screen.blit(status_text, status_position)
            program_cycle = 1

        draw_memory(memory)

        # update screen
        pygame.display.update()

    current_position = get_current_position(memory)
    return skip_size

# create memory from input data
memory = create_memory_block(len(circular_list[0]))

# set the status text position based on the memory size
status_position = set_status_position(memory)

# run part one!
skip_size = run(input_lenghts, skip_size, 1)


num1 = memory[0][0]
num2 = memory[1][0]
part_one = num1 * num2
part_one_answer = ' Part one - Multiplying the first two numbers: ' + str(num1) + ' x ' + str(num2) + ' = ' + str(part_one)
pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
status_text = font3.render(part_one_answer, True, GREEN)
screen.blit(status_text, (status_position[0], status_position[1] + 50))
pygame.display.update()

print(part_one_answer)

pygame.time.wait(1000)

# ---- PART TWO ----

part2_suffix = [17, 31, 73, 47, 23]
input_part2_ascii = [[]]
for c in input_part2:
    input_part2_ascii[0].append(ord(c))

# add the suffix to the input lengths
for s in part2_suffix:
    input_part2_ascii[0].append(s)

# get current position
cur_pos = get_current_position(memory)

# reset the memory
memory = create_memory_block(len(circular_list[0]))
pygame.draw.rect(screen, BLACK, (105, 15, 700, 50))
header_text = font2.render('Advent of Code - day 10 - part 2 (anthorne)', True, WHITE)
draw_memory(memory)
pygame.display.update()
pygame.time.wait(3000)

skip_size = 0

input_lenghts = input_part2_ascii
for r in range(64):
    pygame.draw.rect(screen, BLACK, (105, 15, 700, 50))
    header_text = font2.render('Advent of Code - day 10 - part 2 (anthorne)  run: ' + str(r + 1), True, WHITE)
    screen.blit(header_text, (105, 15))
    skip_size = run(input_lenghts, skip_size, 2000)
    # print(' Run number: ' + str(r) + ' - skip_size: ' + str(skip_size) + ' - current pos: ' + str(get_current_position(memory)))

pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
status_text = font3.render(' Part two - This is the sparse hash', True, WHITE)
screen.blit(status_text, status_position)
pygame.display.update()

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
print(' Part two - The dense hash is: ' + str(dense_hash_hex))
pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
status_text = font3.render(' Part two - The dense hash is: ' + str(dense_hash_hex), True, GREEN)
screen.blit(status_text, (status_position[0], status_position[1] + 70))
pygame.display.update()


pygame.time.wait(10000)
pygame.quit()
