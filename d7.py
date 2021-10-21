# Advent of Code - 2017 day 7

# file_obj = open('d7_example.txt')
file_obj = open('d7_input.txt')


program = list()    # ['name', 'weight', 'parent', ['child_1, child_2, child_3']]]


def find_program(prg, programs):
    found = False
    for p in programs:
        if p[0] == prg:
            found = True
    return found


def update_program(child, parent, programs):
    for p in programs:
        if p[0] == child:
            p[2] = parent


def update_weight(p_name, w_weight, programs):
    for p in programs:
        if p[0] == p_name:
            p[1] = w_weight


def get_root_program(programs):
    for p in programs:
        if p[2] == '':
            return p
    return ['', '', '', ['']]


def update_childs(prog, childs, programs):
    for p in programs:
        if p[0] == prog:
            p[3] = childs


def get_program_weight(prog, programs):
    p_weight = 0
    sub_weight = 0
    for p in programs:
        if p[0] == prog:
            p_weight = int(p[1])
            if p[3] != ['']:
                for c in p[3]:
                    sub_weight += get_program_weight(c, programs)
    total_weight = p_weight + sub_weight
    return total_weight


def get_childs(prog, programs):
    childs = ''
    for p in programs:
        if p[0] == prog:
            if p[3] != ['']:
                childs = p[3]
    return childs


def is_balanced(childs, program):
    result = False
    weights = list()
    # create new temporary list of the childrens weights
    for c in childs:
        w = get_program_weight(c, program)
        weights.append(int(w))
    check = 0
    for w1 in weights:
        check += w1
    check = (check - (weights[0] * len(weights)))
    if check == 0:
        result = True
    return result


def find_unbalanced_child(childs, program):
    new_childs = list()
    odd_child = False, 'not found', 0, 0, 0
    normal_weight = 0
    # create new temporary list of the childrens weights
    for c in childs:
        w = get_program_weight(c, program)
        new_childs.append([int(w), 0, c])
    new_childs.sort()
    # count number of occurances the weight of the childs occur and add it to the temporary list
    for nc in new_childs:
        hits = 0
        for nc2 in new_childs:
            if nc[0] == nc2[0]:
                hits += 1
        nc[1] = hits
    # print('after sorting: ' + str(new_childs))
    # get the weight that most occures in the list
    num_occurances = 0
    for nc4 in new_childs:
        if nc4[1] > num_occurances:
            num_occurances = nc4[1]
    for nc5 in new_childs:
        if nc5[1] == num_occurances:
            normal_weight = nc5[0]
    # get the child with the odd weight from the temporary list
    for nc3 in new_childs:
        if nc3[1] == 1:
            odd_child = True, nc3[2], nc3[0], normal_weight, normal_weight - int(nc3[0])
    return odd_child


# Part one - sort all programs
for line in file_obj:
    p_name = str(str(line).split('(')[0]).strip(' ')
    p_weight = str(str(str(line).split('(')[1]).split(')')[0])
    if find_program(p_name, program):
        update_weight(p_name, p_weight, program)
    else:
        program.append([p_name, p_weight, '', ['']])
    # Check the child-programs
    childs = list()
    if str(line).find('->') > 0:
        childs = str(str(line).split('->')[1]).strip(' ').strip('\n').split(', ')
        update_childs(p_name, childs, program)
        for c_name in childs:
            if find_program(c_name, program):
                update_program(c_name, p_name, program)
            else:
                program.append([c_name, '', p_name, ['']])

# for p in program:
#     print(p)

part_one = get_root_program(program)
print(' Part one - The root program is: ' + str(part_one[0]))


# # start from the root program and get the root program's child's total weight to see which one is unbalanced.


# I am not proud of this code, it looks like shit!
def find_the_balance(prog, prog_list):
    balance_is_found = False
    weight_diff = 0
    final_weight = 0
    p_childs = get_childs(prog, prog_list)
    if not is_balanced(p_childs, prog_list):
        # find the unbalanced child
        found, unbalanced_child, unbalanced_child_weight, normal_weight, weight_diff = find_unbalanced_child(p_childs, prog_list)
        if found:
            # print('A unbalanced child is found: ' + str(unbalanced_child) + ' current weight: ' + str(unbalanced_child_weight) + ' diff from normal weight(' + str(normal_weight) + ') is: ' + str(weight_diff))
            final_weight = unbalanced_child_weight + weight_diff
            for cil in get_childs(unbalanced_child, prog_list):
                final_weight -= get_program_weight(cil, prog_list)
            # print(' -- the unbalanced child: ' + str(unbalanced_child) + ' would have weight: ' + str(final_weight))
            # check if that unbalanced child has sub-childs that are balanced
            sub_childs = get_childs(unbalanced_child, prog_list)
            if is_balanced(sub_childs, prog_list):
                balance_is_found = True
                return balance_is_found, weight_diff, final_weight
            else:
                for c in sub_childs:
                    c_balance, c_weight_diff, c_final_weight = find_the_balance(c, prog_list)
                    if c_balance:
                        return c_balance, c_weight_diff, c_final_weight
    else:
        for pc in p_childs:
            if not is_balanced(get_childs(pc, prog_list), prog_list):
                pc_bal, pc_weight_diff, pc_final_weight = find_the_balance(pc, prog_list)
                if pc_bal:
                    return pc_bal, pc_weight_diff, pc_final_weight
    return balance_is_found, weight_diff, final_weight


part_two = find_the_balance(part_one[0], program)
# print(str(part_two))

print(' Part two - The weight of the unbalanced program would be: ' + str(part_two[2]))
