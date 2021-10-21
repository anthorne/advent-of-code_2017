# Advent of Code - 2017 - day 13
import pygame

# Initialize the game engine
pygame.init()
pygame.display.set_caption('anthorne - Advent of Code')
size = [1200, 800]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Define fonts
pygame.font.init()
font = pygame.font.SysFont('liberationmono', 10, bold=True)
font2 = pygame.font.SysFont('liberationmono', 20, bold=False)
font3 = pygame.font.SysFont('liberationmono', 15, bold=False)

header_text = font2.render('Advent of Code - day 13 - part 1 (anthorne)', True, WHITE)
screen.blit(header_text, (105, 15))
pygame.display.update()

# Read input
fw = list()
max_depth = 0
max_range = 0
counter = 0
f = open('d13_input.txt', 'r')
for r in f:
    fw_depth = int(r.split(': ')[0])
    while fw_depth > counter:
        fw.append([counter, 0, 0, 0, 'down'])
        counter += 1
    if fw_depth > max_depth:
        max_depth = fw_depth
    fw_range = int(r.split(': ')[1].strip())
    if fw_range > max_range:
        max_range = fw_range
    fw.append([fw_depth, fw_range, 0, 0, 'down'])          # depth, range, scanner, packet, heading
    counter += 1
f.close()

# # bring in the packet in the depth = 0!
# fw[0][3] = 1

# debug stuff
for l in fw:
    print(l)

print('max depth: ' + str(max_depth) + ' max range: ' + str(max_range))
# depth + padding = screen width
top_padding = 40
padding = 20
spacing = 2
box_width = int(round((size[0] - (padding * 2)) / max_depth) - 2)
box_height = int(round((size[1] - (top_padding)) / max_range) - 2)
if box_height > box_width:
    box_height = box_width
print(' box width: ' + str(box_width))

run = True
move_packet = True
severity = 0
first_iteration = True
while run:
    # This limits the while loop to x times per second.
    clock.tick(800)

    # check if the user clicked close
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            pygame.quit()  # Flag that we are done so we exit this loop

    # draw the situation
    for layer in fw:
        d = layer[0]    # depth
        r = layer[1]    # range
        s = layer[2]    # scanner   (the current range position of the scanner)
        p = layer[3]    # packet    (0 = no packet / 1 = packet)
        if r != 0:
            for r1 in range(r):
                color = GRAY
                if r1 == s:
                    color = RED
                position = ((d * box_width) + (d * spacing) + padding, (r1 * box_height) + top_padding + (r1 * spacing))
                box = pygame.Rect(position[0], position[1], box_width, box_height)
                pygame.draw.rect(screen, color, box, 0)
                if p == 1 and r1 == 0:
                    text_color = WHITE
                    if p == s:
                        text_color = YELLOW
                        # print(' Collision with scanner depth: ' + str(d) + ' with range: ' + str(r) + ' collision severity: ' + str(d * r))
                        # severity += d * r
                    packet_text = font.render('P', True, text_color)
                    screen.blit(packet_text, (position[0] + 2, position[1]))

        else:
            color = GRAY
            if r == s:
                color = RED
            position = ((d * box_width) + (d * spacing) + padding, top_padding)
            box = pygame.Rect(position[0], position[1], box_width, box_height)
            pygame.draw.rect(screen, color, box, 0)
            if p == 1:
                text_color = WHITE
                if p == s:
                    text_color = YELLOW
                    # print(' Collision with scanner depth: ' + str(d) + ' with range: ' + str(r) + ' collision severity: ' + str(d * r))
                    # severity += d * r
                packet_text = font.render('P', True, text_color)
                screen.blit(packet_text, (position[0] + 2, position[1]))

        pygame.display.update()

    # perform movement
    pygame.time.wait(25)
    if move_packet:
        # move the packet
        if first_iteration:
            fw[0][3] = 1        # add the packet in the first iteration
            packet_ever_found = True
        else:
            packet_ever_found = False
        packet_found = False
        for l in fw:
            if packet_found:
                l[3] = 1
                packet_found = False
            elif l[3] == 1 and not first_iteration:
                packet_found = True
                packet_ever_found = True
                l[3] = 0
            # check if collision with scanner happens
            if l[3] == 1 and l[2] == 0:
                print(' Collision with scanner depth: ' + str(l[0]) + ' with range: ' + str(l[1]) + ' collision severity: ' + str(l[0] * l[1]))
                severity += l[0] * l[1]
        move_packet = False
        first_iteration = False
        if not packet_ever_found:
            run = False

    else:
        # move the scanner
        for l in fw:
            r = l[1]    # r = range
            s = l[2]    # s = scanner
            h = l[4]    # h = heading (where the scanner is going)
            if h == 'down':
                if s == r - 1:
                    l[2] -= 1
                    l[4] = 'up'
                else:
                    l[2] += 1
            elif h == 'up':
                if s == 0:
                    l[2] += 1
                    l[4] = 'down'
                else:
                    l[2] -= 1
        move_packet = True


print(' Part one - Severity is: ' + str(severity))
# Part one - Severity is: 1876

pygame.time.wait(5000)
pygame.quit()

