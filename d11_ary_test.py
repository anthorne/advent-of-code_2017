# Advent of Code - 2017 - day 11

import pygame
import pprint


def get_position(parent, direction):
    x = 0
    y = 0
    if direction == 'n':
        x = 0
        y = -16
    if direction == 'ne':
        x = 16
        y = -8
    if direction == 'se':
        x = 16
        y = 8
    if direction == 's':
        x = 0
        y = 16
    if direction == 'sw':
        x = -16
        y = +8
    if direction == 'nw':
        x = -16
        y = -8
    pos = (parent.position[0] + x, parent.position[1] + y)
    return pos


class Hextile:
    def __init__(self, first=[], *rest, **kwargs):
        if rest:
            self.values = [first]
        else:
            self.values = []
            rest = first

        self.values.extend(list(rest))

        self.id = self.values[0]

        direction = ''
        line_color = (128, 128, 0)

        # print(type(self.values[1]))
        if isinstance(self.values[1], tuple):
            self.position = self.values[1]
        elif isinstance(self.values[1], Hextile):
            self.parent = self.values[1]

        if len(self.values) >= 3:
            direction = self.values[2]
            line_color = self.values[3]
        if direction != '' and isinstance(self.parent, Hextile):
            self.position = get_position(self.parent, direction)

        draw_hex(self.position, str(self.id), line_color)

        # if __debug__:
        #     pprint.pprint(self.values)

    def __iter__(self):
        for elem in self.values:
            yield elem


example = False

# Initialize the game engine
pygame.init()
pygame.display.set_caption('anthorne - Advent of Code - 2017 day 11')
size = [1600, 1000]
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

header_text = font2.render('Advent of Code - day 11 - part 1 (anthorne)', True, WHITE)
screen.blit(header_text, (105, 15))
pygame.display.update()


#
#     b----c
#    /      \
#   a        d
#    \      /
#     f----e
#
def draw_hex(position, id, line_color):
    a = position
    b = (position[0] + 6, position[1] - 8)
    c = (position[0] + 16, position[1] - 8)
    d = (position[0] + 22, position[1])
    e = (position[0] + 16, position[1] + 8)
    f = (position[0] + 6, position[1] + 8)

    pygame.draw.line(screen, line_color, a, origo)

    pygame.draw.line(screen, WHITE, a, b)
    pygame.draw.line(screen, WHITE, b, c)
    pygame.draw.line(screen, WHITE, c, d)
    pygame.draw.line(screen, WHITE, d, e)
    pygame.draw.line(screen, WHITE, e, f)
    pygame.draw.line(screen, WHITE, f, a)
    id_text = font.render(id, True, BLUE)
    screen.blit(id_text, (b[0] + 1, b[1]))
    pygame.display.update()
    return


def run(instructions, speed, line_color):
    # Init variables
    run = True
    clock = pygame.time.Clock()
    id_counter = 1
    inst = 0
    color = 10

    while run:
        # This limits the while loop to x times per second.
        clock.tick(speed)

        if line_color == (0, 250, 0):
            color = 10
        line_color = (0, color, 0)
        color += 1

        # check if the user clicked close
        for event in pygame.event.get():    # User did something
            if event.type == pygame.QUIT:   # If user clicked close
                pygame.quit()               # Flag that we are done so we exit this loop

        hex_tiles.append(Hextile(id_counter, hex_tiles[-1], instructions[inst], line_color))
        id_counter += 1
        inst += 1

        pygame.display.update()     # update screen

        if id_counter > len(instructions):
            run = False


if example:
    instructions = ['sw', 'nw', 'ne', 'n', 'se', 'n']
else:
    file_input = open('d11_input.txt')
    for row in file_input:
        instructions = row.split(',')

print(instructions)


# create the first hex in the center of the screen
# origo = (int(size[0] / 2), int(size[1] / 2))
origo = (0, 0)

hex_tiles = list()
hex_tiles.append(Hextile(0, origo))


run(instructions, 1000, GRAY)

print('The position of the last hex-tile is: ' + str(hex_tiles[-1].position))

# The position of the last hex-tile is: (2390, 2616)


def get_direction_from_position(position):
    direction = 'nw'
    if position[0] > origo[0] and position[1] > origo[1]:
        direction = 'nw'
    elif position[0] < origo[0] and position[1] > origo[1]:
        direction = 'ne'
    elif position[0] < origo[0] and position[1] < origo[1]:
        direction = 'se'
    elif position[0] > origo[0] and position[1] < origo[1]:
        direction = 'sw'
    elif position[0] == origo[0] and position[1] > origo[1]:
        direction = 'n'
    elif position[0] == origo[0] and position[1] < origo[1]:
        direction = 's'
    elif position[0] < origo[0] and position[1] == origo[1]:
        direction = 'se'
    elif position[0] > origo[0] and position[1] == origo[1]:
        direction = 'sw'
    else:
        print(' error, what the fuck to do with position: ' + str(position))
    return direction


def count_steps_back(hextile):
    returning_tiles = list()
    direction = get_direction_from_position(hextile.position)
    returning_tiles.append(Hextile(1, get_position(hextile, direction)))
    new_return_pos = hex_tiles[-1].position
    count = 2
    while new_return_pos != origo:
        direction = get_direction_from_position(new_return_pos)
        new_return_pos = get_position(returning_tiles[-1], direction)
        returning_tiles.append(Hextile(count, new_return_pos))
        count += 1
    return returning_tiles[-1].id


steps_back = count_steps_back(hex_tiles[-1])
print(' Part one - Fewest steps back from the last position is: ' + str(steps_back))


max_distance = 0
furthest_hex_tile = Hextile(0, origo)
for h in hex_tiles:
    x = h.position[0] - origo[0]
    y = h.position[1] - origo[1]
    if x < 0:
        x = x * -1
    if y < 0:
        y = y * -1
    distance = x + y
    # if (x > 2106 or y >= 4636) and max_distance > 6740:
    # if (x > 5600 and y > 9200):   # and max_distance > 6740:
    #         print(' --- found x >= 2106 or y >= 4636 at position: ' + str(h.position) + ' with id: ' + str(h.id) + ' - num steps: ' + str(count_steps_back(h)))
    if distance > max_distance:
        max_distance = distance
        furthest_hex_tile = h
print(' The furthest hex tile is ' + str(furthest_hex_tile.id) + ' at position ' + str(furthest_hex_tile.position) + ' with the distance of: ' + str(max_distance))

# The furthest hex tile is 7034 at position (2106, 4636) with the distance of: 6742

returning_tiles = list()
returning_tiles.append(Hextile(1, get_position(furthest_hex_tile, 'nw')))

new_return_pos = returning_tiles[-1].position
count = 2
while new_return_pos[1] > origo[1]:
    if new_return_pos[0] > origo[0]:
        new_return_pos = get_position(returning_tiles[-1], 'nw')
    else:
        new_return_pos = get_position(returning_tiles[-1], 'n')

    returning_tiles.append(Hextile(count, new_return_pos))
    count += 1

print(' Part two - Number of steps back from the furthest position is: ' + str(returning_tiles[-1].id) + ' <--- not quite right.. fix it!')

# 7034 -- your answer is too high.
# 7033 -- not right
# 1510 -- your answer is too low.
# 1511 -- not right

pygame.time.wait(5000)

pygame.quit()
