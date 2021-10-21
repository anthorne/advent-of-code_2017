# Advent of Code - 2017 - day 12


def add_childs(program, childs):
    for c in childs:
        found = False
        for p in programs[program][1]:
            if c == p:
                found = True
        if not found:
            programs[program][1].append(c)


# Get input data
f = open('d12_input.txt', 'r')
programs = list()
for r in f:
    cs = list(map(int, r.split(' <-> ')[1].strip().split(', ')))
    if int(r.split(' <-> ')[0]) not in cs:
        cs.append(int(r.split(' <-> ')[0]))
    cs.sort()
    programs.append([0, cs])
f.close()

# Check if every program in p[1] --> 'c' has all the p[1] childs in it
for p in programs:
    for c in p[1]:
        add_childs(c, p[1])

# Check for different groups in program collection
signatures = list()
for p in programs:
    p[1].sort()
    sign = ''
    for p2 in p[1]:
        sign += str(p2)
    signatures.append(sign)

print(' Part one - The group of Program ID:0 has: ' + str(len(programs[0][1])) + ' members')
print(' Part two - There are this total number of groups: ' + str(len(list(set(signatures)))))
