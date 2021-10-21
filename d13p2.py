# Advent of Code - 2017 - day 13 - part two - version 2

# Read input
fw = list()
max_depth = 0
max_range = 0
counter = 0
f = open('d13_input.txt', 'r')
# f = open('d13_example.txt', 'r')
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
    fw.append([fw_depth, fw_range, 0, 0, 'down'])  # depth, range, scanner, packet, heading
    counter += 1
f.close()

# Debug mode
debug = True

# Debug stuff
# if debug:
#    for l in fw:
#        print(l)
#    print('max depth: ' + str(max_depth) + ' max range: ' + str(max_range))


# # bring in the packet in the depth = 0!
# fw[0][3] = 1


hits = 0
run = True
move_packet = True
severity = 0
first_iteration = True
iteration = 0
steps = 0
while run:
    # # debug
    # if steps > 1000:
    #     run = False

    # perform movement
    if move_packet:
        # move the packet
        iteration += 1
        steps += 1

        # update the previous packet iteration
        if iteration > 1 and iteration <= max_depth:
            for i in range(iteration, 0, -1):
                fw[i - 1][3] = fw[i - 2][3]
        if iteration > max_depth:
            for i in range(max_depth + 1, 0, -1):
                fw[i - 1][3] = fw[i - 2][3]

        # modified - always add packet based on iteration
        fw[0][3] = iteration        # add a new packet based on iteration

        packet_found = True
        for l in fw:
            # check if collision with scanner happens
            if l[2] == 0 and l[3] != 0 and l[3] != -1:
                # print(' Collision with packet: ' + str(iteration) + ' scanner depth: ' + str(l[0]) + ' with range: ' + str(l[1]) + ' collision severity: ' + str(l[0] * l[1]) + ' after ' + str(steps) + ' steps!')
                l[3] = -1       # Dead packet
                severity += l[0] * l[1]
                hits += 1
        move_packet = False

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

        # draw the situation
        if debug:
            srow = "S: "
            prow = "P: "
            for layer in fw:
                d = layer[0]  # depth
                r = layer[1]  # range
                s = layer[2]  # scanner   (the current range position of the scanner)
                p = layer[3]  # packet    (0 = no packet / 1 = packet)
                if s > 9:
                    srow += str(s) + "|"
                else:
                    srow += " " + str(s) + "|"
                if p > 9:
                    prow += str(p) + "|"
                else:
                    prow += " " + str(p) + "|"
            # print(str(fw))
            print("    Iteration: " + str(iteration))
            # print(str(srow))
            # print(str(prow))
            # print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        # check surviving packet
        if iteration > max_depth:
            if fw[max_depth][3] != -1:
                print("-------------------------------------------------------------------------------------------------")
                print(" First surviving packet through the firewall (after " + str(iteration) + " iterations) is: " + str(fw[max_depth][3]) + " !!")
                print("  Part two - delay should be: " + str(fw[max_depth][3]-1) + " picoseconds!!")
                run = False
