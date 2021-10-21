# Advent of Code - 2017 - day 11
# Checkout: https://www.redblobgames.com/grids/hexagons/

import pygame
# from PIL import Image


def get_coordinates(old_coords, old_position, direction):
    px = 0
    py = 0
    x = 0
    y = 0
    z = 0
    if direction == 'n':
        y = +1
        z = -1
        py = -16
    if direction == 'ne':
        x = +1
        z = -1
        px = 16
        py = -8
    if direction == 'se':
        x = +1
        y = -1
        px = 16
        py = 8
    if direction == 's':
        y = -1
        z = +1
        py = 16
    if direction == 'sw':
        x = -1
        z = +1
        px = -16
        py = +8
    if direction == 'nw':
        x = -1
        y = +1
        px = -16
        py = -8
    new_position = (old_position[0] + px, old_position[1] + py)
    new_coords = (old_coords[0] + x, old_coords[1] + y, old_coords[z] + z)
    return [new_coords, new_position]


class Hextile:
    def __init__(self, id, coordinates, position, color):
        self.id = id
        self.color = color
        self.coordinates = coordinates
        self.position = position
        draw_hex(self.position, str(self.id), color)


# Instructions
example = False
if example:
    instructions = ['se', 'se', 's', 's', 'se', 'se', 'se', 'se', 'se', 'se', 'se', 'se', 'se', 's', 's', 'sw', 'sw', 'nw', 'nw', 'n', 'n', 'sw', 'nw', 'ne', 'n', 'se', 'n']
else:
    file_input = open('d11_input.txt', 'r')
    instructions = file_input.read().split(',')
    file_input.close()


# Alternative solution
f = open("d11_input.txt", "r")
ds = f.read().split(",")
f.close()

x = 0
y = 0
z = 0

dists = []

for d in ds:
  if d == "n":
    y += 1
    z -= 1
  elif d == "s":
    y -= 1
    z += 1
  elif d == "ne":
    x += 1
    z -= 1
  elif d == "sw":
    x -= 1
    z += 1
  elif d == "nw":
    x -= 1
    y += 1
  elif d == "se":
    x += 1
    y -= 1
  dists.append((abs(x) + abs(y) + abs(z)) / 2)

print('Part 1: ' + str((abs(x) + abs(y) + abs(z)) / 2))
print('Part 2: ' + str(max(dists)))


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
def draw_hex(pos, id, color):
    a = pos
    b = (pos[0] + 6, pos[1] - 8)
    c = (pos[0] + 16, pos[1] - 8)
    d = (pos[0] + 22, pos[1])
    e = (pos[0] + 16, pos[1] + 8)
    f = (pos[0] + 6, pos[1] + 8)

    # pygame.draw.line(screen, color, a, (0, 0))

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


def run(instructions, speed, color):
    # Init variables
    run = True
    clock = pygame.time.Clock()
    id_counter = 1
    inst = 0
    c = 10

    while run:
        # This limits the while loop to x times per second.
        clock.tick(speed)

        if color == (0, 250, 0):
            c = 10
        color = (0, c, 0)
        c += 1

        # check if the user clicked close
        for event in pygame.event.get():    # User did something
            if event.type == pygame.QUIT:   # If user clicked close
                pygame.quit()               # Flag that we are done so we exit this loop

        coord_pos = get_coordinates(hex_tiles[-1].coordinates, hex_tiles[-1].position, instructions[inst])
        new_coords = coord_pos[0]
        new_position = coord_pos[1]
        new_hex = Hextile(id_counter, new_coords, new_position, color)
        hex_tiles.append(new_hex)
        id_counter += 1
        inst += 1

        pygame.display.update()     # update screen
        if id_counter > len(instructions):
            run = False


def get_steps_back(coordinates):
    x = abs(coordinates[0])
    y = abs(coordinates[1])
    z = abs(coordinates[2])
    return ((abs(x) + abs(y) + abs(z)) / 2)


# create the first hex in the center of the screen
# origo = (int(size[0] / 2), int(size[1] / 2))
origo = (0, 0)

hex_tiles = list()
hex_tiles.append(Hextile(0, (0, 0, 0), origo, WHITE))

run(instructions, 1000, RED)

print(' Part one - Fewest steps back from the last position is: ' + str(get_steps_back(hex_tiles[-1].coordinates)))

steps_back = 0
steps_back_id = 0
for t in hex_tiles:
    s = get_steps_back(t.coordinates)
    if s > steps_back:
        steps_back = s
        steps_back_id = t.id

print(' Part two - Number of steps back from the furthest position is: ' + str(steps_back) + ' -- ' + str(hex_tiles[steps_back_id].coordinates))

pygame.time.wait(5000)

# img = Image.new('RGB', (width, height))
# img.putdata(image_pixels)
# img.save('image.png')

pygame.quit()
