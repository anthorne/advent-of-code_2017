# Advent of Code - 2017 - day 14
import pygame
import d14_knothash


# Convert hex value to binary
def hex_to_bin(hex_value):
    scale = 16
    binstr = str(bin(int(hex_value, scale)))
    binstr = binstr[2:]
    while len(binstr) < 4:
        binstr = '0' + binstr
    return binstr


# Create a representation of the memory
def create_disk(disk_blocks):
    disk = list()
    padding_top = 40
    padding_sides = 32
    block_size = 6                      # 6 * 128 = 768 (32px left in resolution 800x600)
    row_count = 1
    pos = 0
    row_id = 0
    for row in disk_blocks:
        col_id = 0
        for cell in row:
            if pos == 0:
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
            if cell == '#':
                group_id = 0            # group-id : 0 = used bit with no group
            else:
                group_id = -1           # group-id : -1 = free bit grouping n/a
            disk.append([row_id, col_id, cell, [a, b, c, d], group_id])
            col_id += 1
        row_id += 1
    return disk


# Draw the representation of the disk
def draw_disk(drive):
    # clock = pygame.time.Clock()
    for i in drive:
        # clock.tick(2000)
        a = i[3][0]
        b = i[3][1]
        c = i[3][2]
        d = i[3][3]

        state = i[2]
        text_color = GRAY
        bg_color = BLACK
        if state == '#':
            text_color = WHITE
            bg_color = RED
        if state == '.':
            text_color = WHITE
            bg_color = BLACK

        # fill the background
        pygame.draw.rect(screen, bg_color, (a[0], a[1], b[0] - a[0], b[0] - a[0]))

        # # write the text
        # mem_text = font.render(str(i[2]), False, text_color)
        # screen.blit(mem_text, (a[0] + 4, a[1] + 2))

        # draw the lines
        pygame.draw.line(screen, BLACK, a, b)
        pygame.draw.line(screen, BLACK, b, c)
        pygame.draw.line(screen, BLACK, c, d)
        pygame.draw.line(screen, BLACK, d, a)

        # refresh the display
        pygame.display.update()
    return


# Draw the disk blocks in console based on group
def draw_block_groups(drive):
    print('\n Grouped blocks:\n-------------------------------------------------------')
    bit_counter = 0
    row = ''
    for i in drive:
        if bit_counter > 127:
            bit_counter = 0
            print(str(row))
            row = ''
        if i[4] == -1:         # Group-id -- 0 = no group ; -1 = free bit grouping n/a
            row += '   |'
        else:
            if i[4] < 10:
                row += ' '
            if i[4] < 100:
                row += ' '
            row += str(i[4]) + '|'
        bit_counter += 1
    if row != '':
        print(str(row))
    return True


# Find groups with adjacent sectors
def map_drive(drive):
    grid = [128, 128]
    group_id_counter = 1
    adjacent_cells_to_be_marked = list()
    cells_to_mark = list()

    for drive_cell in drive:
        # # search through the adjacent cells to be marked list and check if cell is present with a group there
        # for listed_cell in adjacent_cells_to_be_marked:
        #     if listed_cell[0] == drive_cell[0] and listed_cell[1] == drive_cell[1]:
        #         if drive_cell[4] == 0:
        #             drive_cell[4] = listed_cell[2]
        #         adjacent_cells_to_be_marked.remove(listed_cell)
        if drive_cell[4] == 0:                # [4] = Group-id
            # Found ungrouped sector
            drive, cells_to_mark = set_group(drive, drive_cell[0], drive_cell[1], group_id_counter, cells_to_mark)
            # adjacent_cells_to_be_marked += [[drive_cell[0], drive_cell[1] + 1, group_id_counter]]     # cell to the right
            # adjacent_cells_to_be_marked += [[drive_cell[0] + 1, drive_cell[1], group_id_counter]]     # cell below
            group_id_counter += 1
    return drive


def get_group_from_cell(row, col, drive):
    for d in drive:
        if len(d) > 3:
            print('drive_ count: ' + str(len(d)))
            if d[0] == row and d[1] == col:
                return d[4]
    return -2


# Function to follow adjacent cells and set group_id
def set_group(drive, row, col, group_id, cells_to_mark):
    # add adjacent cells
    # if row - 1 >= 0:
    #    cells_to_mark += [[row - 1, col, group_id]]
    if row + 1 < 128:
        if get_group_from_cell(row + 1, col, drive) == 0:
            cells_to_mark += [[row + 1, col, group_id]]
    # if col -1 >= 0:
    #    cells_to_mark += [[row, col - 1, group_id]]
    if col + 1 < 128:
        if get_group_from_cell(row, col + 1, drive) == 0:
            cells_to_mark += [[row, col + 1, group_id]]

    # iterate the drive and mark cell
    for drive_cell in drive:
        if drive_cell[0] == row and drive_cell[1] == col:
            if drive_cell[4] == 0:
                drive_cell[4] = group_id
                draw_block_groups(drive)
                # check if cell is present in the list to mark
                for cell_to_mark in cells_to_mark:
                    for dr_cell in drive:
                        if cell_to_mark[0] == dr_cell[0] and cell_to_mark[1] == dr_cell[1]:
                            if dr_cell[4] != 0 and dr_cell[4] != -1:
                                if dr_cell[4] != cell_to_mark[2]:
                                    print(' ERROR: Cell to mark has different group! -> ' + str(cell_to_mark))
                                cells_to_mark.remove(cell_to_mark)
                            break

            elif drive_cell[4] == -1:
                pass
                # print('Adjacent cell: [' + str(row) + ', ' + str(col) + '] is free and will not have a group, skipping...')
            else:
                print('Adjacent cell: [' + str(row) + ', ' + str(col) + '] already belongs to a group!!..')
            break

    # call same function again for rest of the cells to mark
    for cell_to_mark in cells_to_mark:
        drive = set_group(drive, cell_to_mark[0], cell_to_mark[1], cell_to_mark[2], list())

    return drive, cells_to_mark


# --- Day 14: Disk Defragmentation ---
# Disk consist of 128x128 grid
# State (used: 1 or free: 0) of the grid is tracked by the bits in a sequence of knot hashes, row by row
# Hash input are key string: hwlqcszp-0, hwlqcszp-1, hwlqcszp-2, hwlqcszp-..., hwlqcszp-127

# TODO:
#  - PART ONE -
#   - Convert hash input to 32 hexadecimal digits           [x]
#   - Convert 32 hexadecimal digits to disk row 128 bit     [x]
#   - Display 128x128 grid with states                      [x]
#   - Count number of free and used bits                    [x]
#    - PART ONE: How many squares are used?                 [x]
#  - PART TWO -
#   - Map regions                                           [ ]
#   - How many regions are present?                         [ ]


# Initialize the game engine
pygame.init()
pygame.display.set_caption('anthorne - Advent of Code - 2017 - day 14')
size = [800, 900]
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

# Declare variables
testing = False
use_pre_scanned_disk = True
disk_grid = [128, 128]
disk = []

# Test data
if testing:
    test_disk = ['##.#.#..', '.#.#.#.#', '....#.#.', '#.#.##.#', '.##.#...', '##..#..#', '.#...#..', '##.#.##.'] # <-- example data
    puzzle_input = 'flqrgnkx'   # example
else:
    puzzle_input = 'hwlqcszp'   # real challenge

# Convert hash input to 32 hexadecimal digits, and then into 128-bits disk rows
# Open pre-scanned disk
if use_pre_scanned_disk:
    diskfile = open('d14_scanned-disk.txt')
    for filerow in diskfile:
        disk.append(filerow.strip())
else:
    # Scan disk based on puzzle input
    for r in range(disk_grid[1]):
        print(' Scanning disk in progress... ' + str((r / 128) * 100)[:5] + ' %')
        hexa_row = str(d14_knothash.knot(puzzle_input + '-' + str(r)))
        binary_row = ''
        for h in hexa_row:
            binary_row += hex_to_bin(h)
        if len(binary_row) != 128:
            print('Length not ok: ' + str(len(binary_row)) + '\n' + str(binary_row))
        disk.append(binary_row.replace('0', '.').replace('1', '#'))

# Compare test data with example from challenge
if testing:
    print('\n\n')
    for r in range(7):
        if test_disk[r] != disk[r][:8]:
            print(' - Testing row: ' + str(r) + ' -- NOT OK!! Test: ' + str(test_disk[r]) + ' <-> Disk: ' + str(disk[r][:8]))
        else:
            print(' - Testing row: ' + str(r) + ' -- OK!!')
    print('\n\n')

# Create disk
drive = create_disk(disk)

# Display 128x128 grid with states in console and count free/used bits
count_free = 0
count_used = 0
for memrow in disk:
    print(str(memrow))
    for b in memrow:
        if b == '#':
            count_used += 1
        if b == '.':
            count_free += 1

# Answer part one!
print(' Part one - How many squares are used: ' + str(count_used))

# Display in graphical window
header_text = font2.render('Advent of Code - day 14 (anthorne)', True, WHITE)
screen.blit(header_text, (105, 15))
# draw_disk(drive)

# Test draw disk memory groups
draw_block_groups(drive)

# Map groups for drive
drive = map_drive(drive)

# Test draw disk memory groups
draw_block_groups(drive)



pygame.time.wait(10000)
pygame.quit()







# ----------------------------------------------------------------------
#
#
# def get_current_position(memory):
#     pos = int()
#     count = 0
#     for m in memory:
#         if m[2] == 'x':
#             pos = count
#             break
#         count += 1
#     return pos
#
#
# def set_current_position(memory, cur_pos):
#     for m in memory:
#         if m[2] == 'x':
#             m[2] = ''
#             break
#     count = 0
#     for m in memory:
#         if count == cur_pos:
#             m[2] = 'x'
#             break
#         count += 1
#     return
#
#
# def set_status_position(memory):
#     position = [800, 0]
#     for i in memory:
#         if i[1][3][1] > position[1]:
#             position[1] = i[1][3][1]
#         if i[1][3][0] < position[0]:
#             position[0] = i[1][3][0]
#     position[1] = position[1] + 3
#     return position
#
#
# def unselect_memory(memory):
#     for y in memory:
#         if y[2] == 's':
#             y[2] = ''
#
#
# def select_memory(memory, selection_len):
#     # clear old selection
#     unselect_memory(memory)
#     # select new
#     current_pos = int()
#     count = 0
#     for i in memory:
#         if i[2] == 'x':
#             current_pos = count
#         count += 1
#     mem_len = len(memory) - 1
#     counter = current_pos + 1
#     for x in range(selection_len - 1):
#         if counter > mem_len:
#             counter = 0
#         if memory[counter][2] == 'x':
#             print('error!! the selection is bigger than the memory itself! - debug: ' + str(memory))
#         memory[counter][2] = 's'
#         counter += 1
#
#
# def reverse_selected_memory(memory):
#     mem_values = list()
#     mem_positions = list()
#     start_pos = int()
#     x_found = False
#     order = 0
#     pos = 0
#     # look for the beginning of selection = 'x'
#     for m in memory:
#         if m[2] == 'x':
#             mem_values.append(m[0])                     # memory values
#             mem_positions.append([order, pos])          # memory position
#             start_pos = pos
#             x_found = True
#         if x_found and m[2] == 's':
#             mem_values.append(m[0])                     # memory values
#             mem_positions.append([order, pos])          # memory position
#         order += 1
#         pos += 1
#     pos = 0
#     # get the rest of the selected values if any in a second iteration
#     for m in memory:
#         if pos == start_pos:
#             break
#         else:
#             if m[2] == 's' or m[2] == 'x':
#                 mem_values.append(m[0])                     # memory values
#                 mem_positions.append([order, pos])          # memory position
#         order += 1
#         pos += 1
#     mem_positions.sort(reverse=True)
#     v = 0
#     for p in mem_positions:
#         p2 = p[1]
#         memory[p2][0] = mem_values[v]
#         v += 1
#
#
# def perform_selection(memory, step):
#     # get selection length
#     selection_len = -1
#     if len(input_lenghts[0]) > step:
#         selection_len = input_lenghts[0][step]
#     else:
#         return -1
#     step += 1
#     if selection_len != -1:
#         pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 500, 50))
#         status_text = font3.render('The selection lenght is: ' + str(selection_len), True, WHITE)
#         screen.blit(status_text, status_position)
#
#     # select the memory
#     select_memory(memory, selection_len)
#     return step
#
#
# def move_current_position(memory, step, skip_size):
#     steps = input_lenghts[0][step]
#     old_pos = int()
#     counter = 0
#     for m in memory:
#         if m[2] == 'x':
#             old_pos = counter
#             m[2] = ''
#             break
#         counter += 1
#     new_pos = old_pos + steps + skip_size
#     while len(memory) <= new_pos:
#         new_pos = new_pos - len(memory)
#     memory[new_pos][2] = 'x'
#
#
# def run(input_lenghts, skip_size, speed, memory):
#     # Init variables
#     running = True
#     clock = pygame.time.Clock()
#     step = 0
#     program_cycle = 0
#
#     while running:
#         # This limits the while loop to x times per second.
#         clock.tick(speed)
#
#         # check if the user clicked close
#         for event in pygame.event.get():    # User did something
#             if event.type == pygame.QUIT:   # If user clicked close
#                 pygame.quit()               # Flag that we are done so we exit this loop
#
#         # First cycle
#         if program_cycle == 0:
#             pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
#             status_text = font3.render('Instructions: ' + str(input_lenghts), True, WHITE)
#             screen.blit(status_text, status_position)
#             program_cycle += 1
#
#         # Get instruction
#         elif program_cycle == 1:
#             pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
#             if step < len(input_lenghts[0]):
#                 status_text = font3.render('Performing current instruction: ' + str(input_lenghts[0][step]), True, WHITE)
#                 screen.blit(status_text, status_position)
#             program_cycle += 1
#
#         # Select the memory blocks
#         elif program_cycle == 2:
#             step = perform_selection(memory, step)
#             if step == -1:
#                 running = False
#             pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
#             # TODO: Fix error - step 11-1 -- input_lengths[0][10] is out of range
#             # status_text = font3.render('Performing current instruction: ' + str(input_lenghts[0][step - 1]) + ' - Memory selected!', True, WHITE)
#             screen.blit(status_text, status_position)
#             program_cycle += 1
#
#         # Reverse selected memory
#         elif program_cycle == 3:
#             reverse_selected_memory(memory)
#             pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
#             # TODO: Fix error - step 11-1 -- input_lengths[0][10] is out of range
#             # status_text = font3.render('Performing current instruction: ' + str(input_lenghts[0][step - 1]) + ' - Selected memory is reversed!', True, WHITE)
#             screen.blit(status_text, status_position)
#             program_cycle += 1
#
#         # Unselect memory
#         elif program_cycle == 4:
#             unselect_memory(memory)
#             pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
#             program_cycle += 1
#
#         # Move current posision by the selection lenght + skip_size
#         elif program_cycle == 5:
#             move_current_position(memory, step - 1, skip_size)
#             pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
#             status_text = font3.render('Moving to new position!', True, WHITE)
#             screen.blit(status_text, status_position)
#             program_cycle += 1
#
#         # Increase skip_size by +1
#         elif program_cycle == 6:
#             skip_size += 1
#             pygame.draw.rect(screen, BLACK, (status_position[0], status_position[1], 700, 50))
#             status_text = font3.render('Skip size is now increased!', True, WHITE)
#             screen.blit(status_text, status_position)
#             program_cycle = 1
#
#         draw_memory(memory)
#
#         # update screen
#         pygame.display.update()
#
#     current_position = get_current_position(memory)
#     return skip_size, memory
